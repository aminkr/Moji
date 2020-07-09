$(document).ready(function () {

    paypal.Button.render({
        env: 'sandbox', // Or 'production'
        // Set up the payment:
        // 1. Add a payment callback
        payment: function (data, actions) {
            // 2. Make a request to your server
            return actions.request.post('http://0.0.0.0:5000/payment')
                .then(function (res) {
                    // 3. Return res.id from the response
                    return res.paymentID;
                });
        },
        // Execute the payment:
        // 1. Add an onAuthorize callback
        onAuthorize: function (data, actions) {
            // 2. Make a request to your server
            return actions.request.post('http://0.0.0.0:5000/execute', {
                paymentID: data.paymentID,
                payerID: data.payerID
            })
                .then(function (res) {
                    // 3. Show the buyer a confirmation message.
                    // print(res.success)
                });
        }
    }, '#paypal-button');

});