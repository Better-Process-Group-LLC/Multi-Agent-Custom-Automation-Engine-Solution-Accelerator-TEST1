#!/bin/bash




SUBSCRIPTION_ID="${AZURE_SUBSCRIPTION_ID}"
GPT_MIN_CAPACITY="${GPT_MIN_CAPACITY}"
AZURE_CLIENT_ID="${AZURE_CLIENT_ID}"
AZURE_TENANT_ID="${AZURE_TENANT_ID}"
AZURE_CLIENT_SECRET="${AZURE_CLIENT_SECRET}"
AZURE_LOCATION="${AZURE_LOCATION}"



echo "🔄 Validating required environment variables..."
if [[ -z "$SUBSCRIPTION_ID" || -z "$GPT_MIN_CAPACITY" || -z "$AZURE_LOCATION" ]]; then
    echo "❌ ERROR: Missing required environment variables."
    exit 1
fi

echo "🔄 Setting Azure subscription..."
if ! az account set --subscription "$SUBSCRIPTION_ID"; then
    echo "❌ ERROR: Invalid subscription ID or insufficient permissions."
    exit 1
fi
echo "✅ Azure subscription set successfully."

# Define models and their minimum required capacities
declare -A MIN_CAPACITY=(
    ["OpenAI.GlobalStandard.gpt-4o"]=$GPT_MIN_CAPACITY
)


echo "----------------------------------------"
echo "🔍 Checking location: $AZURE_LOCATION"


    QUOTA_INFO=$(az cognitiveservices usage list --location "$AZURE_LOCATION" --output json)
    if [ -z "$QUOTA_INFO" ]; then
        echo "⚠️ WARNING: Failed to retrieve quota for location $AZURE_LOCATION."
        exit 1
    fi


    INSUFFICIENT_QUOTA=false
    for MODEL in "${!MIN_CAPACITY[@]}"; do
        MODEL_INFO=$(echo "$QUOTA_INFO" | awk -v model="\"value\": \"$MODEL\"" '
            BEGIN { RS="},"; FS="," }
            $0 ~ model { print $0 }
        ')

        if [ -z "$MODEL_INFO" ]; then
            echo "⚠️ WARNING: No quota information found for model: $MODEL in $AZURE_LOCATION. Skipping."
            continue
        fi

        CURRENT_VALUE=$(echo "$MODEL_INFO" | awk -F': ' '/"currentValue"/ {print $2}' | tr -d ',' | tr -d ' ')
        LIMIT=$(echo "$MODEL_INFO" | awk -F': ' '/"limit"/ {print $2}' | tr -d ',' | tr -d ' ')

        CURRENT_VALUE=${CURRENT_VALUE:-0}
        LIMIT=${LIMIT:-0}

        CURRENT_VALUE=$(echo "$CURRENT_VALUE" | cut -d'.' -f1)
        LIMIT=$(echo "$LIMIT" | cut -d'.' -f1)

        AVAILABLE=$((LIMIT - CURRENT_VALUE))

        echo "✅ Model: $MODEL | Used: $CURRENT_VALUE | Limit: $LIMIT | Available: $AVAILABLE"

        if [ "$AVAILABLE" -lt "${MIN_CAPACITY[$MODEL]}" ]; then
            echo "❌ ERROR: $MODEL in $AZURE_LOCATION has insufficient quota."
            INSUFFICIENT_QUOTA=true
            break
        fi
    done

    if [ "$INSUFFICIENT_QUOTA" = false ]; then
        echo "✅ Location $AZURE_LOCATION has sufficient quota."
        exit 0
    else
        echo "❌ Location $AZURE_LOCATION does not have sufficient quota. Blocking deployment."
        echo "QUOTA_FAILED=true" >> "$GITHUB_ENV"
        exit 0
    fi