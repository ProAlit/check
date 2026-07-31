name: downloader-kick

on:
  workflow_dispatch:
    inputs:
      url:
        description: >
          Enter one or more Kick VOD/Clip URLs.
          Separate by commas, spaces, or newlines.
        required: true
      quality:
        description: 'Video quality (leave empty for best available)'
        type: choice
        required: false
        options:
          - ''                 # best available (default)
          - 1080p60
          - 1080p
          - 720p60
          - 720p
          - 480p
          - 360p
          - 160p
          - audio_only
      bundle_all:
        description: 'Bundle all downloaded files into a single ZIP archive'
        type: boolean
        default: false
      upload_method:
        description: 'Upload destination'
        required: true
        type: choice
        options:
          - repo
          - release
          - drive
        default: repo
      vpn_enabled:
        description: 'Route downloads through WireGuard VPN (requires secret WG_CONFIG)'
        type: boolean
        default: false
      concurrent_downloads:
        description: 'Number of URLs to download at the same time'
        type: number
        default: 4
        required: false

permissions:
  contents: write

jobs:
  actions:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: true

      - name: Install dependencies
        run: |
          sudo apt-get update -qq
          sudo apt-get install -y -qq ffmpeg jq curl

      - name: Get kick-dl CLI
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          echo "→ Fetching latest release info..."
          RELEASE_JSON=$(curl -sS -H "Authorization: Bearer $GH_TOKEN" \
            https://api.github.com/repos/juliogarciape/kick-dl/releases/latest)
          if ! echo "$RELEASE_JSON" | jq -e '.assets' > /dev/null 2>&1; then
            echo "❌ Failed to fetch release info"
            exit 1
          fi
          ASSET_NAME=$(echo "$RELEASE_JSON" | jq -r '.assets[].name' | grep -E 'linux.*amd64|Linux.*x86_64' | head -1)
          if [ -z "$ASSET_NAME" ]; then
            echo "❌ Could not find Linux amd64 asset"
            exit 1
          fi
          DOWNLOAD_URL=$(echo "$RELEASE_JSON" | jq -r --arg name "$ASSET_NAME" '.assets[] | select(.name==$name) | .browser_download_url')
          echo "→ Downloading $ASSET_NAME ..."
          curl -sSL -o kickdl_archive "$DOWNLOAD_URL"
          if [[ "$ASSET_NAME" == *.zip ]]; then
            unzip -q kickdl_archive -d kickdl_extracted
          else
            mkdir -p kickdl_extracted
            tar xf kickdl_archive -C kickdl_extracted
          fi
          BINARY_PATH=$(find kickdl_extracted -type f -name 'kick-dl' -o -name 'kick-dl*' | head -1)
          if [ -z "$BINARY_PATH" ]; then
            echo "❌ Could not find kick-dl binary in archive"
            exit 1
          fi
          chmod +x "$BINARY_PATH"
          sudo mv "$BINARY_PATH" /usr/local/bin/kick-dl
          rm -rf kickdl_archive kickdl_extracted
          echo "✅ kick-dl CLI ready"

      - name: Parse URLs
        id: parse
        run: |
          URLS_INPUT="${{ github.event.inputs.url }}"
          URLS=$(echo "$URLS_INPUT" | tr ',' ' ' | tr '\n' ' ' | tr -s ' ' | sed 's/^ *//;s/ *$//')
          if [ -z "$URLS" ]; then
            echo "No URLs provided." >&2
            exit 1
          fi
          echo "$URLS" | tr ' ' '\n' > urls.txt
          echo "URLs to download:"
          cat urls.txt
          NUM=$(wc -l < urls.txt)
          echo "NUM_URLS=$NUM" >> $GITHUB_OUTPUT

      - name: 'Set up WireGuard VPN (if enabled)'
        id: vpn
        shell: bash
        run: |
          VPN_ENABLED="${{ inputs.vpn_enabled }}"
          echo "VPN_ENABLED=$VPN_ENABLED"
          if [ "$VPN_ENABLED" = "true" ]; then
            if [ -z "${{ secrets.WG_CONFIG }}" ]; then
              echo "VPN enabled but WG_CONFIG secret is empty – VPN disabled for this run."
              echo "vpn_available=false" >> $GITHUB_OUTPUT
              exit 0
            fi
            echo "→ Installing WireGuard tools..."
            sudo apt-get update -qq
            sudo apt-get install -y -qq wireguard-tools openresolv 2>/dev/null || sudo apt-get install -y -qq wireguard-tools
            echo "→ Writing WireGuard config..."
            cat <<'EOF' > /tmp/wg0.conf
          ${{ secrets.WG_CONFIG }}
          EOF
            sudo cp /tmp/wg0.conf /etc/wireguard/wg0.conf
            sudo chmod 600 /etc/wireguard/wg0.conf
            echo "→ Bringing up wg0..."
            if sudo wg-quick up wg0; then
              echo "WireGuard VPN connected."
              echo "vpn_available=true" >> $GITHUB_OUTPUT
            else
              echo "Failed to bring up WireGuard – VPN disabled."
              sudo wg-quick down wg0 2>/dev/null || true
              echo "vpn_available=false" >> $GITHUB_OUTPUT
            fi
          else
            echo "vpn_available=false" >> $GITHUB_OUTPUT
          fi

      - name: Download all Kick videos concurrently
        run: |
          set -e
          VPN_AVAILABLE="${{ steps.vpn.outputs.vpn_available }}"
          CONCURRENT="${{ inputs.concurrent_downloads }}"
          OUTPUT_DIR="kick"
          FAILED_FILE="failed_urls.txt"
          mkdir -p "$OUTPUT_DIR"
          > "$FAILED_FILE"

          download_one() {
            local url="$1"
            local sanitized=$(echo "$url" | md5sum | cut -c1-12)
            local outfile="${OUTPUT_DIR}/kick_${sanitized}.mp4"
            echo "→ Downloading: $url"
            QUALITY_ARG=""
            if [ -n "${{ inputs.quality }}" ]; then
              QUALITY_ARG="-q ${{ inputs.quality }}"
            fi
            # Adjust flags if kick-dl uses different ones
            if kick-dl -u "$url" -o "$outfile" --ffmpeg-path /usr/bin/ffmpeg $QUALITY_ARG; then
              echo "✅ Success: $url -> $outfile"
            else
              echo "❌ Download failed: $url"
              echo "$url" >> "$FAILED_FILE"
              rm -f "$outfile" 2>/dev/null || true
            fi
          }
          export -f download_one
          export OUTPUT_DIR FAILED_FILE VPN_AVAILABLE
          echo "→ Starting parallel downloads (concurrency: $CONCURRENT, VPN: $VPN_AVAILABLE)"
          cat urls.txt | xargs -P "$CONCURRENT" -I '{}' bash -c 'download_one "{}"'
          echo "📊 Downloads finished."
          ls -la "$OUTPUT_DIR/"
        shell: bash

      - name: Zip and bundle files
        run: |
          BUNDLE_ALL="${{ github.event.inputs.bundle_all }}"
          UPLOAD_METHOD_INPUT="${{ inputs.upload_method }}"
          if [ "$UPLOAD_METHOD_INPUT" = "repo" ]; then
            SPLIT_SIZE="99m"
          elif [ "$UPLOAD_METHOD_INPUT" = "release" ]; then
            SPLIT_SIZE="1950m"
          else
            SPLIT_SIZE="none"
          fi
          OUTPUT_DIR="kick"
          FAILED_FILE="failed_urls.txt"
          if [ -s "$FAILED_FILE" ]; then
            RAND_FAIL=$(mktemp -u XXXXX)
            FAIL_NAME="links-failed-${RAND_FAIL}.txt"
            mv "$FAILED_FILE" "${OUTPUT_DIR}/$FAIL_NAME"
            echo "Created failure report: ${OUTPUT_DIR}/$FAIL_NAME"
          else
            rm -f "$FAILED_FILE"
          fi
          if [ "$BUNDLE_ALL" = "true" ]; then
            BUNDLE_DIR="bundle_contents"
            mkdir -p "$BUNDLE_DIR"
            cp "$OUTPUT_DIR"/* "$BUNDLE_DIR/" 2>/dev/null || true
            if [ -n "$(ls -A "$BUNDLE_DIR" 2>/dev/null)" ]; then
              RAND_BUNDLE=$(mktemp -u XXXXX)
              BUNDLE_ZIP="kick_${RAND_BUNDLE}.zip"
              echo "Creating bundle: $BUNDLE_ZIP"
              if [ "$SPLIT_SIZE" = "none" ]; then
                (cd "$BUNDLE_DIR" && zip -0 "../${OUTPUT_DIR}/${BUNDLE_ZIP}" *)
              else
                (cd "$BUNDLE_DIR" && zip -0 "../${OUTPUT_DIR}/${BUNDLE_ZIP}" *)
                FULLBUNDLE="${OUTPUT_DIR}/${BUNDLE_ZIP}"
                SIZE=$(stat -c%s "$FULLBUNDLE" 2>/dev/null || echo 0)
                if [ "$SIZE" -gt $(( $(echo "$SPLIT_SIZE" | sed 's/m//') * 1048576 )) ]; then
                  echo "Bundle ZIP larger than limit, splitting"
                  rm "$FULLBUNDLE"
                  (cd "$BUNDLE_DIR" && zip -0 -s "$SPLIT_SIZE" "../${OUTPUT_DIR}/${BUNDLE_ZIP}" *)
                fi
              fi
              rm -rf "$BUNDLE_DIR"
              echo "→ Removing original media files (keeping only the bundle ZIP)"
              find "$OUTPUT_DIR" -type f ! -name "*.zip" ! -name "*.txt" -delete
            else
              echo "No files to bundle."
              rm -rf "$BUNDLE_DIR"
            fi
          else
            for f in "$OUTPUT_DIR"/*; do
              [ -f "$f" ] || continue
              fname=$(basename "$f")
              RAND5=$( (tr -dc 'a-z' </dev/urandom || true) | head -c5 )
              ZIP_BASE="${fname}_${RAND5}"
              ZIP_NAME="${ZIP_BASE}.zip"
              echo "Zipping: $fname → $ZIP_NAME"
              TMPZIP="tmpzip_$$"
              mkdir -p "$TMPZIP"
              cp "$f" "$TMPZIP/"
              if [ "$SPLIT_SIZE" = "none" ]; then
                (cd "$TMPZIP" && zip -0 "../${OUTPUT_DIR}/${ZIP_NAME}" "$fname")
              else
                (cd "$TMPZIP" && zip -0 "../${OUTPUT_DIR}/${ZIP_NAME}" "$fname")
                FULLZIP="${OUTPUT_DIR}/${ZIP_NAME}"
                SIZE=$(stat -c%s "$FULLZIP" 2>/dev/null || echo 0)
                if [ "$SIZE" -gt $(( $(echo "$SPLIT_SIZE" | sed 's/m//') * 1048576 )) ]; then
                  echo "ZIP larger than limit, splitting"
                  rm "$FULLZIP"
                  (cd "$TMPZIP" && zip -0 -s "$SPLIT_SIZE" "../${OUTPUT_DIR}/${ZIP_NAME}" "$fname")
                fi
              fi
              rm -rf "$TMPZIP"
            done
          fi
          ls -1 "$OUTPUT_DIR" > "${OUTPUT_DIR}_assets.txt"
          echo "Assets to upload:"
          cat "${OUTPUT_DIR}_assets.txt"
        shell: bash

      - name: 'Disconnect VPN for uploads'
        if: steps.vpn.outputs.vpn_available == 'true'
        run: |
          echo "→ Bringing down WireGuard to use runner's native internet for uploads"
          sudo wg-quick down wg0

      - name: "Upload to Google Drive"
        if: inputs.upload_method == 'drive'
        env:
          CLIENT_ID:     ${{ secrets.GOOGLE_CLIENT_ID }}
          CLIENT_SECRET: ${{ secrets.GOOGLE_CLIENT_SECRET }}
          REFRESH_TOKEN: ${{ secrets.GOOGLE_REFRESH_TOKEN }}
        run: |
          ACCESS_TOKEN=$(curl -s -X POST https://oauth2.googleapis.com/token \
            -d client_id="$CLIENT_ID" \
            -d client_secret="$CLIENT_SECRET" \
            -d refresh_token="$REFRESH_TOKEN" \
            -d grant_type=refresh_token | jq -r '.access_token')
          if [ -z "$ACCESS_TOKEN" ] || [ "$ACCESS_TOKEN" = "null" ]; then
            echo "❌ Failed to obtain access token"
            exit 1
          fi
          FOLDER_NAME="github-actions"
          QUERY="mimeType='application/vnd.google-apps.folder' and name='$FOLDER_NAME' and trashed=false"
          FOLDER_ID=$(curl -s -G \
            -H "Authorization: Bearer $ACCESS_TOKEN" \
            --data-urlencode "q=$QUERY" \
            --data-urlencode "fields=files(id)" \
            "https://www.googleapis.com/drive/v3/files" | jq -r '.files[0].id // ""')
          if [ -z "$FOLDER_ID" ]; then
            echo "→ Creating folder '$FOLDER_NAME'"
            FOLDER_ID=$(curl -s -X POST \
              -H "Authorization: Bearer $ACCESS_TOKEN" \
              -H "Content-Type: application/json" \
              -d "{\"name\":\"$FOLDER_NAME\", \"mimeType\":\"application/vnd.google-apps.folder\"}" \
              "https://www.googleapis.com/drive/v3/files?fields=id" | jq -r '.id')
            if [ -z "$FOLDER_ID" ] || [ "$FOLDER_ID" = "null" ]; then
              echo "❌ Failed to create folder"
              exit 1
            fi
          fi
          echo "✅ Folder ID: $FOLDER_ID"
          OUTPUT_DIR="kick"
          for file in "$OUTPUT_DIR"/*; do
            [ -f "$file" ] || continue
            fname=$(basename "$file")
            size=$(stat -c%s "$file")
            echo "→ Uploading $fname ($size bytes)..."
            SESSION_URI=$(curl -s -X POST \
              -H "Authorization: Bearer $ACCESS_TOKEN" \
              -H "Content-Type: application/json; charset=UTF-8" \
              -H "X-Upload-Content-Type: application/zip" \
              -d "{\"name\":\"$fname\", \"parents\":[\"$FOLDER_ID\"]}" \
              "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable" \
              -D - | tr -d '\r' | grep -i '^location:' | sed 's/^location: //i' | tr -d ' ')
            if [ -z "$SESSION_URI" ]; then
              echo "❌ Failed to initiate upload session for $fname, skipping"
              continue
            fi
            HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
              -H "Authorization: Bearer $ACCESS_TOKEN" \
              -H "Content-Length: $size" \
              -H "Content-Range: bytes 0-$((size-1))/$size" \
              --upload-file "$file" \
              "$SESSION_URI")
            if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 201 ]; then
              echo "✅ Uploaded $fname"
            else
              echo "❌ Upload failed with HTTP $HTTP_CODE"
            fi
          done

      - name: Upload to repository (split_push method)
        if: ${{ inputs.upload_method == 'repo' }}
        env:
          BRANCH: ${{ github.ref_name }}
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git config http.postBuffer 524288000
          OUTPUT_DIR="kick"
          if [ -z "$(ls -A "$OUTPUT_DIR/")" ]; then
            echo "No files to upload."
            exit 0
          fi
          git add "$OUTPUT_DIR/"
          COMMIT_MSG="Add: $(ls -1 "$OUTPUT_DIR/" | tr '\n' ' ' | sed 's/ *$//') [skip ci]"
          git commit -m "$COMMIT_MSG" || echo "Nothing to commit"
          RETRIES=5
          for i in $(seq 1 $RETRIES); do
            echo "Push attempt $i..."
            git pull --rebase --autostash origin "$BRANCH"
            if git push origin "$BRANCH"; then
              echo "Push succeeded."
              break
            else
              [ $i -lt $RETRIES ] && sleep 3 || exit 1
            fi
          done

      - name: Create Release and upload assets (release method)
        if: ${{ inputs.upload_method == 'release' }}
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          OUTPUT_DIR="kick"
          if [ ! -s "${OUTPUT_DIR}_assets.txt" ]; then
            echo "No assets to release."
            exit 0
          fi
          RAND5=$(mktemp -u XXXXX)
          TAG="kick-downloader-${RAND5}"
          echo "Creating release tag: $TAG"
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git tag "$TAG" -m "Kick download release"
          git push origin "$TAG"
          ASSET_ARGS=""
          while IFS= read -r file; do
            ASSET_ARGS="$ASSET_ARGS ${OUTPUT_DIR}/$file"
          done < "${OUTPUT_DIR}_assets.txt"
          gh release create "$TAG" $ASSET_ARGS \
            --title "kick-downloader-${RAND5}" \
            --notes "Automated release from Kick Downloader workflow." \
            --target "${{ github.ref_name }}"

      - name: Cleanup
        if: always()
        run: |
          rm -rf kick urls.txt failed_urls.txt kick_assets.txt 2>/dev/null || true
          sudo wg-quick down wg0 2>/dev/null || true