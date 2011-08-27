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
    $("#users-index").dataTable({
        bJQueryUI: true,
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
});
