$(".spinner").hide();
$(".test-content").hide();

var path_name = window.location.pathname;
var scripts_path = "../scripts/";
var app_token = "";
var project_src_test_json_string;
var third_party_plugins_test_json_string;

function check_for_saved_tests(){

    // get token from project's token file
    $.get(scripts_path + "app_token", function(token){

        app_token = token;

        //gets json strings from local storage
        project_src_test_json_string = localStorage.getItem('project_src_test_' + app_token);
        third_party_plugins_test_json_string = localStorage.getItem('third_party_plugins_test_' + app_token);


        // initialize dashboard functions when windows.location.pathname is equals to index page
        if(path_name === '/index.php' || path_name === '/'){

          if(project_src_test_json_string !== null){
              generate_test(
                  "#project_test", 
                  project_src_test_json_string, 
                  'project_src_test'
                  );
          }

          if(third_party_plugins_test_json_string !== null){
              generate_test(
                  "#third_party_test", 
                  third_party_plugins_test_json_string, 
                  'third_party_plugins_test'
                  );
          }

        }

        // initialize dashboard functions when windows.location.pathname is equals to project-code-test.php
        else if(project_src_test_json_string !== null && 
            path_name === '/project-code-test.php'){

        generate_test(
            "#project_test", 
            project_src_test_json_string, 
            'project_src_test'
            );
        }
        // initialize dashboard functions when windows.location.pathname is equals to project-code-test.php
        else if(third_party_plugins_test_json_string !== null && 
            path_name === '/third-party-plugins-test.php'){

            generate_test(
                "#third_party_test", 
                third_party_plugins_test_json_string, 
                'third_party_plugins_test'
                );
        }
        // initialize dashboard functions when windows.location.pathname is equals to file-details.php
        else if(path_name === '/file-details.php'){
            render_file_details();
            hljs.initHighlighting();
            $('[data-toggle="popover"]').popover();

            $(".file-warnings, .file-errors").addClass("pointable");

            $(".file-warnings").on("click",function(){
                $("html body").animate({
                    scrollTop: $("code.warning").offset().top - 75
                },1000);
            });

            $(".file-errors").on("click",function(){
                $("html body").animate({
                    scrollTop: $("code.error").offset().top - 75
                },1000);
            });
        }
    });
}


//on click event for project test 
$("#project_test button").on("click", function(){

    var parent_name = "#project_test";

    test_button_event_on_click(
        parent_name,
        'project_src_test'
        );
});


//on click event for third party test 
$("#third_party_test button").on("click", function(){
    var parent_name = "#third_party_test";

    test_button_event_on_click(
        parent_name,
        'third_party_plugins_test'
        );
});


//on click action for run test buttons
function test_button_event_on_click(parent_name, report_type){
    $(parent_name + " .test-content").hide();

    $(parent_name + " .spinner").show();
    $(parent_name + " button").attr("disabled", true);

    $.get( 
        scripts_path + "get_tests_json.php",
        {
            report_type: report_type
        })
    .done(function(json_string) {

        json = JSON.parse(json_string);

        //apending lines information for tested files
        json = append_lines_tested_information(json);

        json_string = JSON.stringify(json);

        var now = new Date();
        localStorage.setItem(report_type + "_" + app_token, json_string);
        localStorage.setItem(report_type + "_datetime_" + app_token, now.toString());

        generate_test(parent_name, json_string, report_type);

    })
    .fail(function() {
        $(parent_name + " .quick_stats").html("Error while runing the test").fadeIn();
        $(parent_name + " .spinner").hide();
        $(parent_name + " button").attr("disabled", false);
    });
}


//generates information for test
function generate_test(parent_name, json_string, report_type){

    json = JSON.parse(json_string);

    var quick_stats = generate_quick_stats_information(json);

    // generate data template for canvas
    var data = generate_canvas_data(
            quick_stats.total_corrects,
            quick_stats.total_warnings,
            quick_stats.total_errors
            );

    $(parent_name + " .quick_stats").html(render_quick_stats(quick_stats, report_type));

    if(path_name !== '/index.php' && path_name !== '/'){
        $(parent_name + " .test-content").append(render_details_template(json.files, report_type));
    }

    $(parent_name + " .test-content").fadeIn();

    var ctx = $(parent_name + " canvas").get(0).getContext("2d");
    var configurations = generate_canvas_configurations();

    var myDoughnut = new Chart(ctx).Doughnut(data, configurations);

    $(parent_name + " .spinner").hide();
    $(parent_name + " button").attr("disabled", false);

    switch_run_test_button(parent_name,true);
}


// renders template with given quick stats
function render_quick_stats(quick_stats, report_type){

    var score_color_class = "";
    var qualitative_score = "Qualitative score";
    var date_template = "";

    if(quick_stats.score < 25){
        score_color_class = "light-red-text";
        qualitative_score = "Kill it before it lays eggs";
    }
    else if(quick_stats.score < 50){
        score_color_class = "red-text";
        qualitative_score = "This needs more attention to details";
    }
    else if(quick_stats.score <= 80){
        score_color_class = "orange-text";
        qualitative_score = "You can do it better";
    }
    else if(quick_stats.score <= 99){
        score_color_class = "green-text";
        qualitative_score = "Almost beautiful";
    }
    else if(quick_stats.score === 100){
        score_color_class = "blue-text";
        qualitative_score = "You're the best!";
    }

    var saved_report_date = localStorage.getItem(report_type + '_datetime');

    if(saved_report_date != null){
        date_template = "<hr/>                                                                                                              \
        Last time runned: <strong>" + saved_report_date + "</strong>";
    }

    template = "<div>                                                                                                                       \
    <h3 class='score " + score_color_class + "'>                                                                                            \
    " + qualitative_score + "                                                                                                               \
    <span>(" + quick_stats.score + "%)</span>                                                                                               \
    </h3>                                                                                                                                   \
    <hr/>                                                                                                                                   \
    <h4>Quick stats</h4>                                                                                                                    \
    Total files checked: <strong>" + quick_stats.total_files + "</strong>";

    if(path_name !== '/index.php' && path_name !== '/'){

        template += "<hr/>                                                                                                                  \
        Files correct: <strong>" + quick_stats.files_correct.length + "</strong><br/>                                                       \
        Files incorrect: <strong>" + quick_stats.files_incorrect.length + "</strong><br/>                                                   \
        Files with warnings: <strong>" + quick_stats.files_with_warnings.length + "</strong><br/>                                           \
        Files with errors: <strong>" + quick_stats.files_with_errors.length + "</strong>";
    }

    template +="<hr>                                                                                                                        \
    Total lines checked: <strong>" + quick_stats.total_lines + "</strong><br/>                                                              \
    Total correct: <strong>" + quick_stats.total_corrects + " <i>(" + quick_stats.corrects_porcentage_value + "%)</i></strong><br/>         \
    Total warnings: <strong>" + quick_stats.total_warnings + " <i>(" + quick_stats.warnings_porcentage_value + "%)</i></strong><br/>        \
    Total errors: <strong>" + quick_stats.total_errors + " <i>(" + quick_stats.errors_porcentage_value + "%)</i></strong>                   \
    " + date_template + "                                                                                                                   \
    </div>";

    return template;
}


// renders template for test file details
function render_details_template(json_files, report_type){
    
    var template = "";

    template = "<hr/>                                                                                                                       \
    <div class='test-details'>                                                                                                              \
    <h4>Details</h4>                                                                                                                        \
    <div class='panel-group' role='tablist'>";

    $.each(json_files, function(file_path, file_info) {

        var file_stats_template = render_file_stats(file_info);

        var n = Math.floor((Math.random() * 10000) + 1);

        template += "<a class='collapsed test-file'                                                                                         \
            href='file-details.php?file_path=" + file_path + "&report_type=" + report_type + "'>                                            \
            <div class='panel panel-default'>                                                                                               \
                <div class='panel-heading' role='tab' id='headingThree'>                                                                    \
                    <h4 class='panel-title col-sm-10'>                                                                                      \
                        <span class='glyphicon glyphicon-file' aria-hidden='true'></span>                                                   \
                        " + generate_fixed_file_name(file_path) + "                                                                         \
                    </h4>                                                                                                                   \
                    " + file_stats_template + "                                                                                             \
                </div>                                                                                                                      \
            </div>                                                                                                                          \
        </a>";
    });

    template += "</div></div>";

    return template;
}

function render_file_details(){
    var json;

    if(report_type === 'project_src_test'){
        json = JSON.parse(project_src_test_json_string);
    }
    else if(report_type === 'third_party_plugins_test'){
        json = JSON.parse(third_party_plugins_test_json_string);
    }

    var file_info = _.find(json.files, function(file_info, file_name){
        return file_name == file_path;
    });

    var file_stats_template = render_file_stats(file_info);
    var title_template = "<div class='name col-sm-9'>" 
            + generate_fixed_file_name(file_path) 
        + "</div>" 
        + file_stats_template; 

    $("#file-name-title").append(title_template);

    var template = "<table class='table table-hover'>                                                                                       \
      <tbody>";

    var file_json = append_file_information_to_json(file_path, file_info.messages);

    var file_extension = file_path.split('.').pop();

    $.each(file_json, function(i, message_info) {

        if(message_info.line_content !== ''){
            var message_class = "";
            var background_color = "";
            var popover = "";

            if(message_info.type === 'ERROR'){
                message_class="danger";
                background_color="error";
            }
            else if(message_info.type === 'WARNING'){
                message_class='warning';
                background_color="warning";
            }

            if(message_info.type == 'ERROR' || message_info.type == 'WARNING'){
                popover = " tabindex='0'                                                                                                    \
                    data-html='true'                                                                                                        \
                    data-toggle='popover'                                                                                                   \
                    data-placement='top'                                                                                                    \
                    data-trigger='hover'                                                                                                    \
                    title='Description'                                                                                                     \
                    data-content='" + message_info.message + "'";
            }

            template +="<tr class='" + message_class + "'>                                                                                  \
                  <td class ='table-details-nline' scope='row'>" + (message_info.line + 1) + "</td>                                         \
                  <td class='table-details-code'>                                                                                           \
                    <pre" + popover + "><code class='" + 
                    background_color + " " + 
                    file_extension + "'>" + 
                    message_info.line_content + "</code></pre>                                                                              \
                  </td>                                                                                                                     \
                </tr>";
        }
    });

    template +="</tbody>                                                                                                                    \
        </table>";

    $("#file-details-list").html(template);
}

function render_file_stats(file_info){
    var template = "";

    var warnings_tag = "";
    var errors_tag = "";
    var correct_tag = "";
    
    if(file_info.warnings > 0){
        warnings_tag = "<div class='file-warnings text-center' title='warnings'>Warnings: " 
        + file_info.warnings 
        + "</div>";
    }
    if(file_info.errors > 0){
        errors_tag = "<div class='file-errors text-center' title='errors'>Errors: " 
        + file_info.errors 
        + "</div>";
    }
    if(file_info.errors === 0 && file_info.warnings === 0){
        correct_tag = "<div class='file-correct text-center' title='warnings'>                                                          \
        <span class='glyphicon glyphicon-ok'></span>                                                                                    \
    </div>";
    }

    template = "<div class='file-details text-right'>                                                                                   \
            " + warnings_tag + "                                                                                                        \
            " + errors_tag + "                                                                                                          \
            " + correct_tag + "                                                                                                         \
        </div>";

    return template;
}


// generates quick stats information with given json
function generate_quick_stats_information(json){

    var stats = {};

    stats.total_files = json.totals.files_tested;

    stats.total_lines = json.totals.lines_tested;

    stats.files_with_errors = _.filter(json.files, function(item){
        return item.errors > 0;
    });

    stats.files_with_warnings = _.filter(json.files, function(item){
        return item.warnings > 0;
    });

    stats.files_correct = _.filter(json.files, function(item){
        return item.warnings == 0 && item.warnings == 0;
    });

    stats.files_incorrect = _.filter(json.files, function(item){
        return item.warnings > 0 && item.warnings > 0;
    });

    //porcentage
    var error_weight = 1;
    var warning_weight = 1;

    stats.one_percent_value = 100 / stats.total_lines;
    
    stats.total_corrects = stats.total_lines - (json.totals.errors + json.totals.warnings)
    stats.total_errors = json.totals.errors;
    stats.total_warnings = json.totals.warnings;

    stats.corrects_porcentage_value = parseFloat((stats.total_corrects * stats.one_percent_value).toFixed(2));
    stats.errors_porcentage_value = parseFloat((stats.total_errors * (stats.one_percent_value * error_weight)).toFixed(2));
    stats.warnings_porcentage_value = parseFloat((stats.total_warnings * (stats.one_percent_value * warning_weight)).toFixed(2));
    
    stats.wrong_porcentage_value = stats.errors_porcentage_value + stats.warnings_porcentage_value;
    stats.score = (100 - stats.wrong_porcentage_value).toFixed(2);

    return stats;
}


// returns information object for canvas graph
function generate_canvas_data(total_corrects, total_warnings, total_errors){
    var data = [
    {
        color: "#46BFBD",
        highlight: "#5AD3D1",
        label: "Lines correct"
    },
    {
        color: "#FDB45C",
        highlight: "#FFC870",
        label: "Lines with warnings"
    },
    {
        color:"#DA5556",
        highlight: "#FF5A5E",
        label: "Lines with errors"
    }
    ];

    data[0].value = total_corrects;
    data[1].value = total_warnings;
    data[2].value = total_errors;

    return data;
}


// returns information object with configurations for canvas graph
function generate_canvas_configurations() {

    var configurations = {
        responsive: true,
        segmentShowStroke : true,
        segmentStrokeColor : "#fff",
        segmentStrokeWidth : 2,
        percentageInnerCutout : 0, 
        animationSteps : 100,
        animationEasing : "easeOutBounce",
        animateRotate : true,
        animateScale : false,
        legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"
    };

    return configurations;
}


//fix file path that will be showed
function generate_fixed_file_name(file_path){
    return file_path.replace("/home/vagrant/", "");
}


// appends file lines that doesn't exist in json information
function append_file_information_to_json(file_path, file_info_messages){
    var text_file = "No available";

    $.ajax(
        {
            url: scripts_path + "get_file_json.php",
            data: {
                file_path: file_path
            },
            async: false
        }
    ).done(function(string_file) {
        text_file = string_file;
    });

    var lines = text_file.split("\n");

    // fixing number of line for hints
    $.each(file_info_messages, function(i,line){
        file_info_messages[i].line = file_info_messages[i].line -1;
    });

    $.each(lines, function(i,line){

            if(!_.find(file_info_messages, 'line', i)){
                if(line.length > 0){
                    var no_hints_line = {};
                   
                    no_hints_line.line = i;
                    no_hints_line.line_content = _.escape(line);
                    no_hints_line.message = "";
                    no_hints_line.severity = "";

                    file_info_messages.push(no_hints_line);
                }
            }
            else{
                var message = "";
                var cur_obj;

                var line_repetitions = _.filter(file_info_messages, function(obj, n){
                    return obj.line == i;
                });
                 
                $.each(line_repetitions, function(i,obj){                 
                    obj.line_content = line;
                    cur_obj = obj;
                    message += _.escape("<strong>" + obj.message + "</strong>.<br/><i>Column: " + obj.column 
                        + "</i><br/><i>Severity: " + obj.severity + "</i><hr/> ");

                    if (i != line_repetitions.length - 1) {
                        obj.line_content = "";
                    }
                });

                cur_obj.message = message;
            }
    });
    return _.sortByOrder(file_info_messages, 'line', true);
}


// Gets count information from given json, and includes it to json object
function append_lines_tested_information(json){
    var total_lines = 0;
    var total_files = 0;

    $.each(json.files, function(file_path, file_content){
         $.ajax(
            {
                url: scripts_path + "test_count_lines.php",
                data: {
                    file_path: file_path
                },
                async: false
            }
        ).done(function(file_lines_count) {
            lines_count = parseInt(file_lines_count);

            file_content.lines_count = lines_count;
            total_lines+=lines_count;
            total_files++;
        });
    });

    json.totals.lines_tested = total_lines;
    json.totals.files_tested = total_files;

    return json;
}


// Changes buttons text if text was runned
function switch_run_test_button(parent_name, was_runned){
    if(was_runned){
        if(path_name === '/index.php' || path_name === '/'){
            $(parent_name + " .test-header a").html(
                "<span class='glyphicon glyphicon-eye-open'></span> View details"
                );
        }
        else{
            $(parent_name + " button").html(
                "<span class='glyphicon glyphicon-refresh'></span> Run test again"
                );
        }
        $(parent_name + ' .test-never-runned').hide();
    }
}

check_for_saved_tests();
