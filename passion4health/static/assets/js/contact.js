$(document).ready(function () {

    (function ($) {
        "use strict";

        // Custom validator method
        jQuery.validator.addMethod('answercheck', function (value, element) {
            return this.optional(element) || /^\bcat\b$/.test(value);
        }, "type the correct answer -_-");

        // Validate contactForm form
        $(function () {
            $('#contactForm').validate({
                rules: {
                    name: {
                        required: true,
                        minlength: 2
                    },
                    subject: {
                        required: true,
                        minlength: 4
                    },
                    number: {
                        required: true,
                        minlength: 5
                    },
                    email: {
                        required: true,
                        email: true
                    },
                    message: {
                        required: true,
                        minlength: 4
                    }
                },
                messages: {
                    name: {
                        required: "Your name is required please!",
                        minlength: "your name must consist of at least 2 characters"
                    },
                    subject: {
                        required: "The subject of the message is required!",
                        minlength: "your subject must consist of at least 4 characters"
                    },
                    number: {
                        required: "come on, you have a number, don't you?",
                        minlength: "your Number must consist of at least 5 characters"
                    },
                    email: {
                        required: "no email, no message"
                    },
                    message: {
                        required: "um...yea, you have to write something to send this form.",
                        minlength: "that's all? really?"
                    }
                },

                submitHandler: function (form) {
                    // Disable the submit button and change its text to "..."
                    var $submitButton = $(form).find('button[type="submit"]');
                    $submitButton.prop('disabled', true).text('...');

                    // Trigger reCAPTCHA programmatically before submitting
                    grecaptcha.ready(function () {
                        grecaptcha.execute('6LexcFgqAAAAAD0hX7KsiMfZtQ5SdFbs3HIRF4Ru', { action: 'submit' }).then(function (token) {
                            // Add the reCAPTCHA token to the form
                            $('<input>').attr({
                                type: 'hidden',
                                name: 'recaptcha_token',
                                value: token
                            }).appendTo('#contactForm');

                            // Use FormData to properly submit the form
                            var formData = new FormData(form);

                            $.ajax({
                                type: "POST",
                                url: $('#contactForm').attr("action"),
                                data: formData,
                                processData: false, // Prevent jQuery from automatically transforming the data into a query string
                                contentType: false, // Tell jQuery not to set content type header
                                success: function () {
                                    $('#contactForm :input').attr('disabled', 'disabled');
                                    $('#contactForm').fadeTo("slow", 1, function () {
                                        $(this).find(':input').attr('disabled', 'disabled');
                                        $(this).find('label').css('cursor', 'default');
                                        $('#success').fadeIn();
                                        $('.modal').modal('hide');
                                        $('#success').modal('show');
                                    });
                                    $('#contactForm').trigger("reset");
                                },
                                error: function () {
                                    $('#contactForm').fadeTo("slow", 1, function () {
                                        $('#error').fadeIn();
                                        $('.modal').modal('hide');
                                        $('#error').modal('show');
                                    });
                                },
                                complete: function () {
                                    // Re-enable the submit button and restore its text
                                    $submitButton.prop('disabled', false).text('Send');
                                }
                            });
                        });
                    });
                }

            });
        });

    })(jQuery);
});
