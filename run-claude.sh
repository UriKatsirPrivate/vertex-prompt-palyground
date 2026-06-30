# gcloud auth login
export CLAUDE_CODE_USE_VERTEX=1
export ANTHROPIC_VERTEX_PROJECT_ID="landing-zone-demo-341118"
export CLOUD_ML_REGION="global"
export CLAUDE_CODE_EFFORT_LEVEL=xhigh

# Trust corporate proxy / MDM root CAs from the macOS keychain.
# Node ships its own CA store and ignores the keychain by default, so traffic
# through the corp proxy fails with "SSL certificate verification failed".
# Export the keychain roots to a bundle and point Node at it.
CA_BUNDLE="$HOME/.config/node-ca-bundle.pem"
mkdir -p "$(dirname "$CA_BUNDLE")"
{ security find-certificate -a -p /Library/Keychains/System.keychain
  security find-certificate -a -p /System/Library/Keychains/SystemRootCertificates.keychain
} > "$CA_BUNDLE" 2>/dev/null
export NODE_EXTRA_CA_CERTS="$CA_BUNDLE"

gcloud auth application-default login
"$(dirname "$0")/setup-data-sharing.sh"
npx @anthropic-ai/claude-code