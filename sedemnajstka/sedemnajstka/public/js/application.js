var dataTableTranslation = {
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
};

$(function() {
    $.datepicker.setDefaults($.datepicker.regional["sl"])
    $(".datepicker").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd.mm.yy",
        maxDate: new Date().getDate(),
        minDate: new Date(1253941200 * 1000)
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

        iso_start = $.datepicker.formatDate("yy-mm-dd", $.datepicker.parseDate("dd.mm.yy", start));
        iso_end = $.datepicker.formatDate("yy-mm-dd", $.datepicker.parseDate("dd.mm.yy", end));

        user_id = $("#ppdow-user-id").val();

        $("#ppdow-tabs").tabs("add", "/users/" + user_id + "/charts/ppdow/start/" + iso_start + "/end/" + iso_end, start + "–" + end);
        return false;
    });

    $("#pph-do").click(function () {
        start = $("#pph-start-date").val();
        end = $("#pph-end-date").val();

        iso_start = $.datepicker.formatDate("yy-mm-dd", $.datepicker.parseDate("dd.mm.yy", start));
        iso_end = $.datepicker.formatDate("yy-mm-dd", $.datepicker.parseDate("dd.mm.yy", end));

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
    $("#users-index").dataTable({
        bJQueryUI: true,
        iDisplayLength: 25,
        oLanguage: dataTableTranslation,
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

    $("#players").dataTable({
        bJQueryUI: true,
        iDisplayLength: 10,
        oLanguage: dataTableTranslation,
        sPaginationType: "full_numbers"
    });

    // Date range slider
    $("#date-range").slider({
        animate: true,
        max: new Date().getTime() / 1000, // today
        min: 1253941200,                  // when we started
        range: true,
        step: 86400,            // one day in seconds
        values: [1253941200, new Date().getTime() / 1000],
        create: function(ev, ui) {
            $(this).slider("values", 0, $.datepicker.parseDate("dd.mm.yy", $("#from").val()) / 1000);
            $(this).slider("values", 1, $.datepicker.parseDate("dd.mm.yy", $("#to").val()) / 1000);
        },
        slide: function(ev, ui) {
            $("#from").val($.datepicker.formatDate("dd.mm.yy", new Date(ui.values[0] * 1000)));
            $("#to").val($.datepicker.formatDate("dd.mm.yy", new Date(ui.values[1] * 1000)));
        }
    });

    $("#from").change(function () {
        $("#date-range").slider("values", 0, $.datepicker.parseDate("dd.mm.yy", $("#from").val()) / 1000);
    });
    $("#to").change(function () {
        $("#date-range").slider("values", 1, $.datepicker.parseDate("dd.mm.yy", $("#to").val()) / 1000);
    });

    $("#date-range-form").submit(function () {
        $("#from").val($.datepicker.formatDate("yy-mm-dd", $.datepicker.parseDate("dd.mm.yy", $("#from").val())));
        $("#to").val($.datepicker.formatDate("yy-mm-dd", $.datepicker.parseDate("dd.mm.yy", $("#to").val())));
    });

    // Archive view controls
    $("#archive_limit").change(function() {
        var limit = $("#archive_limit option:selected").val();
        $.cookie("archive_limit", limit, {expires: 365});
        location.reload();
    });

    $("#archive-view-radio").buttonset();
    $("#compact-view").button({icons: {primary: "my-icon-compact-view"}, text: false});
    $("#full-view").button({icons: {primary: "my-icon-full-view"}, text: false});

    $("#compact-view").click(function () {
        $.cookie("archive_view", "compact", {expires: 365});
        location.reload();
    });

    $("#full-view").click(function () {
        $.cookie("archive_view", "full", {expires: 365});
        location.reload();
    });

    // Summary of topics with qTip
    $(".topic-summary").each(function () {
        $(this).qtip({
            content: {
                url: $(this).attr("href") + "/summary"
            },

            position: {
                corner: {
                    tooltip: "leftMiddle",
                    target: "rightMiddle"
                }
            },
            style: {
                name: "dark",
                tip: true,
            },

            show: {
                effect: {
                    type: "fade",
                    length: 200
                }
            },
            hide: {
                effect: {
                    type: "fade",
                    length: 200
                }
            },
        });
    });

    // Sexy password strength meter
    $("#passwd, #new_passwd").nakedPassword({
        path: "/images/"
    });
});
