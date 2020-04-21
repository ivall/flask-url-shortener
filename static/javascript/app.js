$(document).ready(function() {
    $(document).on("click", ".short", function () {
        var longurl = $("#url").val();

        $.ajax({
            url: '/short',
            type: 'POST',
            data: {longurl : longurl},
            success: function (data) {
                $("#url").val("");
                $('.information').text("Twój skrócony link:");
                $(".link").text("https://shorty.ct8.pl/"+data.shorturl);
                $(".link").prop("href", "https://shorty.ct8.pl/"+data.shorturl);

            }
        });
    });
});