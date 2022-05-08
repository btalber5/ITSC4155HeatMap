$(document).ready(function() {
    console.log("Ready!");


    // Manage edit-name-button text
    $('#edit-name').on('hide.bs.collapse', function() {
        $('a.edit-name-button').html("Edit");
    });
    $('#edit-name').on('show.bs.collapse', function() {
        $('a.edit-name-button').html("Close");
    });


    // Validate password
    $("#submit-button").click(function(event) {
        var pass = $("#pass").val();
        var confirmation = $("#confirmation").val();
        var regex = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,32}$/;
        if (!pass.match(regex)) {
            event.preventDefault();
            alert("Password must be 8-32 characters long and contain at least one number and one special character.");
        } else if (pass != confirmation) {
            event.preventDefault();
            alert("Password and confirmation do not match. Please re-enter them and try again.");
        }
    });


    // Resend validation email
    $("a.verify-button").click(function(event) {
        event.preventDefault();
        $(this).html("Sending email");
        $(this).css('pointer-events', 'none');
        $(this).addClass("text-muted");
        $.post("/verify", $("form.verify-form").serialize())
            .done(function(response) {
                console.log(response);
                $("a.verify-button").html("Email sent");
            })
            .fail(function(response) {
                console.log(response)
            });
    });

});