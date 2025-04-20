<?php
function fetchLastSession() {
    $url = "http://localhost:3000/sessions/last";
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);

    if (curl_errno($ch)) {
        error_log("Erreur cURL (fetchLastSession) : " . curl_error($ch));
        curl_close($ch);
        return null;
    }

    curl_close($ch);

    // Log de la réponse brute pour débogage
    error_log("Réponse brute de fetchLastSession : " . $response);

    $decodedResponse = json_decode($response, true);

    if (json_last_error() !== JSON_ERROR_NONE) {
        error_log("Erreur de décodage JSON (fetchLastSession) : " . json_last_error_msg());
        return null;
    }

    // Log de la réponse décodée pour débogage
    error_log("Réponse décodée de fetchLastSession : " . print_r($decodedResponse, true));

    return $decodedResponse;
}
?>