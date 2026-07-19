class FailureClassifier:
    """
    Classifies AI provider errors into platform-independent categories.

    The goal of this component is to isolate provider-specific
    error messages from the rest of the application.

    Providers may return completely different exceptions, but
    the Router and Priority Manager should operate on a common
    set of failure reasons.
    """

    # Unified platform error types

    RATE_LIMIT = "rate_limit"
    PROVIDER_ERROR = "provider_error"
    INVALID_MODEL = "invalid_model"
    TIMEOUT = "timeout"
    CONTEXT_TOO_LARGE = "context_too_large"
    AUTHENTICATION = "authentication"
    QUOTA_EXCEEDED = "quota_exceeded"
    NETWORK = "network"
    UNKNOWN = "unknown"

    def classify(self, error: Exception) -> str:
        """
        Returns a unified failure reason.
        """

        message = str(error).lower()

        # ----------------------------------------------------------
        # Rate limit
        # ----------------------------------------------------------

        if (
            "429" in message
            or "rate limit" in message
            or "rate-limit" in message
            or "temporarily rate-limited" in message
            or "retry-after" in message
        ):
            return self.RATE_LIMIT

        # ----------------------------------------------------------
        # Quota exceeded
        # ----------------------------------------------------------

        if (
            "free-models-per-day" in message
            or "quota" in message
            or "credits" in message
        ):
            return self.QUOTA_EXCEEDED

        # ----------------------------------------------------------
        # Invalid model
        # ----------------------------------------------------------

        if (
            "404" in message
            or "model not found" in message
            or "unknown model" in message
        ):
            return self.INVALID_MODEL

        # ----------------------------------------------------------
        # Authentication
        # ----------------------------------------------------------

        if (
            "401" in message
            or "unauthorized" in message
            or "authentication" in message
            or "invalid api key" in message
        ):
            return self.AUTHENTICATION

        # ----------------------------------------------------------
        # Timeout
        # ----------------------------------------------------------

        if (
            "timeout" in message
            or "timed out" in message
            or "504" in message
        ):
            return self.TIMEOUT

        # ----------------------------------------------------------
        # Context too large
        # ----------------------------------------------------------

        if (
            "context length" in message
            or "maximum context" in message
            or "too many tokens" in message
        ):
            return self.CONTEXT_TOO_LARGE

        # ----------------------------------------------------------
        # Network
        # ----------------------------------------------------------

        if (
            "connection" in message
            or "network" in message
            or "dns" in message
        ):
            return self.NETWORK

        # ----------------------------------------------------------
        # Provider internal error
        # ----------------------------------------------------------

        if (
            "provider returned error" in message
            or "500" in message
            or "502" in message
            or "503" in message
        ):
            return self.PROVIDER_ERROR

        # ----------------------------------------------------------

        return self.UNKNOWN