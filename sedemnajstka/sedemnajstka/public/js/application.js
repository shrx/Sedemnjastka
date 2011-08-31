$(function() {
    $.datepicker.setDefaults($.datepicker.regional["sl"])
    $(".datepicker").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "d.m.yy"
    });

    $("input:submit").button();

    // Tabs for charts
    $("#ppdow-tabs, #pph-tabs").tabs({
        cache: true,
        selected: 4,

        add: function(ev, ui) {
            $(this).tabs('select', ui.panel.id);
        }
    });

    $("#ppdow-do").click(function () {
        start = $("#ppdow-start-date").val();
        end = $("#ppdow-end-date").val();

        iso_start = $.datepicker.formatDate("yy-mm-dd", $.datepicker.parseDate("d.m.yy", start));
        iso_end = $.datepicker.formatDate("yy-mm-dd", $.datepicker.parseDate("d.m.yy", end));

        user_id = $("#ppdow-user-id").val();

        $("#ppdow-tabs").tabs("add", "/users/" + user_id + "/charts/ppdow/start/" + iso_start + "/end/" + iso_end, start + "–" + end);
        return false;
    });

    $("#pph-do").click(function () {
        start = $("#pph-start-date").val();
        end = $("#pph-end-date").val();

        iso_start = $.datepicker.formatDate("yy-mm-dd", $.datepicker.parseDate("d.m.yy", start));
        iso_end = $.datepicker.formatDate("yy-mm-dd", $.datepicker.parseDate("d.m.yy", end));

        user_id = $("#pph-user-id").val();

        $("#pph-tabs").tabs("add", "/users/" + user_id + "/charts/pph/start/" + iso_start + "/end/" + iso_end, start + "–" + end);
        return false;
    });

    // Login dialog
    $("#login-dialog").dialog({
        autoOpen: false,
        modal: true
    })
    $("#open-login-dialog").click(function () {
        $("#login-dialog").dialog("open");
        return false;
    });

    // User avatar history
    $("#load-avatar-history").one("click", function () {
        $.ajax({
            url: $(this).attr("href"),
            success: function(html) {
                $("#avatar-history").append(html);
            }
        });
        $(this).removeAttr("href");
        return false;
    });

    // users-index DataTable
    $("#users-index, #players").dataTable({
        bJQueryUI: true,
        iDisplayLength: 25,
        oLanguage: {
	    "sProcessing":   "Obdelujem...",
	    "sLengthMenu":   "Prikaži _MENU_ zapisov",
	    "sZeroRecords":  "Noben zapis ni bil najden",
	    "sInfo":         "Prikazanih od _START_ do _END_ od skupno _TOTAL_ zapisov",
	    "sInfoEmpty":    "Prikazanih od 0 do 0 od skupno 0 zapisov",
	    "sInfoFiltered": "(filtrirano po vseh _MAX_ zapisih)",
	    "sInfoPostFix":  "",
	    "sSearch":       "Išči:",
	    "sUrl":          "",
	    "oPaginate": {
		"sFirst":    "Prva",
		"sPrevious": "Nazaj",
		"sNext":     "Naprej",
		"sLast":     "Zadnja"
	    }
        },
        sPaginationType: "full_numbers"
    });

    // Avatar guessing game
    $(".guess").live("click", function () {
        $(".guess").attr("disabled", true); // Disable resubmit cheat
        $(this).attr("id", "guessed");
        var form = $("#ga-form");
        // Append user_id to form
        $("<input>").attr({
            name: "user_id",
            value: $(this).attr("value"),
            type: "hidden"
        }).appendTo(form);
        $("<input>").attr({name: "ajax", value: true,
                           type: "hidden"}).appendTo(form);

        $.post(form.attr("action"), form.serialize(), function(data) {
            var animation = "blind";
            var avatar_guess = $(data);
            var color = "#DE3163";
            if ($(".correct-guess", avatar_guess).length != 0) {
                color = "#BFFF00";
            }

            $("#guessed").css("background-image", "none");
            $("#guessed").animate({backgroundColor: color}, 900, function () {
                // Hide old and fetch new
                $("#guess-avatar").hide(animation, {}, 900, function () {
                    // Insert result of this round into history
                    // See if last history item was even/odd, and reverse ours
                    if ($("#guessing-history tr:first").hasClass("even")) {
                        $(avatar_guess, "tr").addClass("odd");
                    } else {
                        $(avatar_guess, "tr").addClass("even");
                    }
                    avatar_guess.prependTo($("#guessing-history"));

                    // Load new question
                    $("#guess-avatar").empty();
                    $.get("/games/guess-avatar", {ajax: true}, function(data) {
                        $(data).appendTo($("#guess-avatar"));
                        $("#guess-avatar").show(animation, {}, 900);
                    });
                });
            });
        });
        return false;
    });

    // Date range slider
    $("#date-range").slider({
        max: new Date().getTime() / 1000, // today
        min: 1253941200,                  // when we started
        range: true,
        step: 86400,            // one day in seconds
        values: [new Date($("#from").val()) / 1000,
                 new Date($("#to").val()) / 1000],
        slide: function(ev, ui) {
            $("#from").val($.datepicker.formatDate("yy-mm-dd", new Date(ui.values[0] * 1000)));
            $("#to").val($.datepicker.formatDate("yy-mm-dd", new Date(ui.values[1] * 1000)));
        }
    });
});
