
 $(document).ready(function(){

        var w_size;

        $('#upload').on('change', function () {
            var reader = new FileReader();
            reader.onload = function (e) {

                var img = new Image();
                img.src = e.target.result;

                img.onload = function () {
                    w_size = Math.min(img.width, img.height);

                    if (w_size > 600) {
                        w_size = 600;
                    }

                    $uploadCrop.croppie('destroy');

                    $uploadCrop = $('#upload-demo').croppie({
                        enableExif: true,
                        viewport: {
                            width: w_size,
                            height: w_size,
                            type: 'square'
                        },
                        boundary: {
                            width: 600,
                            height: 600
                        },
                        enableZoom: true,
                        enforceBoundary: true
                    });

                    $uploadCrop.croppie('bind', {
                        url: e.target.result,
                        zoom: 0
                    }).then(function () {
                        console.log('jQuery bind complete');
                    });
                };
            };
            reader.readAsDataURL(this.files[0]);
        });


        $uploadCrop = $('#upload-demo').croppie({
            enableExif: true,
            viewport: {
                width: 300,
                height: 300,
                type: 'square'
            },
            boundary: {
                width: 600,
                height: 600
            },
            enableZoom: true,
            enforceBoundary: true
        });

        $('.upload-result').on('click', function (ev) {
            $uploadCrop.croppie('result', {
                type: 'canvas',
                size: 'viewport'
            }).then(function (resp) {
                $.ajax({
                    type: 'POST',
                    url: '/api/predict',
                    data: resp,
                    dataType: 'json',
                    contentType: false,
                    cache: false,
                    async: false,
                    success: function (resp) {
                        console.log(resp);
                        $("#status").text(resp);
                    },
                });
            });
        });
 $(".cr-image").prop("alt", "");
 });