$(document).ready(function () {

     // append four table cells to the row we created
    paypal.Button.render({

        env: 'sandbox', // Or 'production'
        // Set up the payment:
        // 1. Add a payment callback
        payment: function (data, actions) {
            // 2. Make a request to your server
            return actions.request.post('http://0.0.0.0:5000/payment')
                .then(function (res) {
                    // 3. Return res.id from the response
                    if (res.have_credit == true){
                        alert('You have credit')
                        return ;
                    }
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
                    // print(res.success)
                    if (res.success == true){

                       // location.reload(true);
                       $(' <tr style="background: rgba(0,255,127,0.47)">' +
                            '<td> ' + res.data.user_name + '</td>\n' +
                            '<td>' + res.data.date + '</td>\n' +
                            '<td>' + res.data.time + '</td>\n' +
                            '<td>' + res.data.expire_date + '</td>\n' +
                            '<td>' + res.data.amount + '</td>' +
                           '</tr>').prependTo('.balance-table tbody');
                    }
                    else {
                        alert(res.message);
                    }
                });
        }
    }, '#paypal-button');

});