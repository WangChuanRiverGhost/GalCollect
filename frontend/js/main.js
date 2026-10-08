
//储存用户交互

//关于用户输入
var $choose_source = $("#choose_source");
var $choose_cngal_type = $("#choose_cngal_type");
var $choose_cngal_second_type = $("#choose_week_year");
var $choose_cngal_weekly_page = $("#choose_cngal_weekly_page")
var $choose_year = $("#choose_cngal_week_year")
var $start_page = $("#start_cngal_weekly_page");
var $end_page = $("#end_cngal_weekly_page");

var $choose_condition_a = $("#choose_condition_a")
var $choose_condition_b = $("#choose_condition_b")
var $choose_condition_c = $("#choose_condition_c")

//关于用户点击的按钮
var $start_collect = $("#start_collect")  //获取开始采集按钮
var $collect_history = $("#collect_history")  //获取采集历史按钮
var $clear_log = $("#clear_log")  //获取清空日志按钮

//关于用户点击的路径
$("#myTable").on("click", ".file-path", function() {
    var path = $(this).text().trim();  // 获取该单元格文本（文件路径）
    console.log(path);
});   

$(function(){

    $("#choose_cngal_type,#choose_condition_a,#choose_condition_b,#choose_condition_c,#show_table,#show_file").hide()

    //设置用户交互事件
    //监控下拉框选项
    $choose_source.on("change", function(){
        show_filter_criteria($(this).val());
    });

    $choose_cngal_type.on("change",function(){
        show_choose_week_year($(this).val())
    })
    //监控按钮：开始采集
    $start_collect.on("click",function(){

        var data = getFormData()
        $("#show_table").show()

        window.alert("已经获取数据："+ data)

        //把data传到后端处理，发起调用爬虫脚本并解析数据到json文件的请求
        fetch("/start_spider?year=" + data.year + "&page_start=" + data.page_start + "&page_end=" + data.page_end + "&category=" + data.choose_cngal_second_type)
            .then(res=>res.json())
            .then(()=>fetch("/get_table?tp=" + "work_artices")//向后端发送读取work_artices文件中的数据的请求，并展示到前端
                    .then(res=>res.json())
                    .then(data=>{
                        data.forEach(item => {
                            $("#cngal_weekly_table").append(
                                `<tr><td>${item.title}</td><td>${item.url}</td><td>${item.maintext_path}</td>`
                            )

                    });})
        )
        
        window.alert("调用成功")


        

    })
})