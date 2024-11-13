document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const tweetInput = document.getElementById('tweet-input');
    const predictBtn = document.getElementById('predict-btn');
    const predictionResult = document.getElementById('prediction-result');

    // Predict Sentiment Function
    function predictSentiment(tweet) {
        // Simulate sentiment analysis (This should ideally be done with a real model)
        const positiveWords = ['happy', 'great', 'awesome', 'good'];
        const negativeWords = ['bad', 'sad', 'terrible', 'awful'];

        const words = tweet.toLowerCase().split(' ');
        const positiveMatches = words.filter(word => positiveWords.includes(word)).length;
        const negativeMatches = words.filter(word => negativeWords.includes(word)).length;

        if (positiveMatches > negativeMatches) {
            return 'Positive';
        } else if (negativeMatches > positiveMatches) {
            return 'Negative';
        } else {
            return 'Neutral';
        }
    }

    // Event Listener for the Predict Button
    predictBtn.addEventListener('click', () => {
        const tweet = tweetInput.value.trim();
        if (tweet) {
            const sentiment = predictSentiment(tweet);
            predictionResult.innerHTML = `Predicted Sentiment: <strong>${sentiment}</strong>`;
        } else {
            alert('Please enter a tweet.');
        }
    });
});
