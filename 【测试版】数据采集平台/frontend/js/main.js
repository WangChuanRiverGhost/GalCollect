
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

//定时器
let autoScroll = true;
let offset = 0;
function logging(){

    fetch("/get_log?offset=" + offset)  //向后端发送一个定时器
        .then(res=>res.json())
        .then(data=>{
            data.forEach(item=>{
                $("#lower_part").append(
                `<div class="log">${item.content}</div>`
                )
                offset = item.new_offset
           })
                if(autoScroll){
                    $("#lower_part").scrollTop($("#lower_part")[0].scrollHeight);
                }
                setTimeout(logging,100)  
        })

}
$(document).on("click", function (e) {
    // 如果点击的不是正文区域，也不是触发展示的表格单元格
    if (!$(e.target).closest("#show_file").length && 
        !$(e.target).closest(".file_path").length) {
        $("#show_file").hide();
        $("#show_table").css("width", "100%");   // 表格恢复全宽
    }
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
        if(data == null){
            window.alert("有未填写的数据，请继续输入")
            return
        }
        if ($("#cngal_weekly_table tbody").children().length > 0) {
            let c = confirm("检测到有最近的爬取记录，是否保留？（点击确定将保留历史查找，并将本次查找追加至末尾；取消则清空历史查找）\n注：该历史查找指当前页面展示在表格中的数据，非保存在数据库中的数据，需要调取历史查询过，且不在该页面上的数据，请点击【历史查询】")
            if(c){

            }else{
                $("#show_table table tbody").remove()
            }
        } else {
            
        }        
        $("#show_table").show()

        autoScroll = true;
        logging()

        //把data传到后端处理，发起调用爬虫脚本并解析数据到json文件的请求
        fetch("/start_spider?year=" + data.year + "&page_start=" + data.page_start + "&page_end=" + data.page_end + "&category=" + data.choose_cngal_second_type)
            .then(res=>res.json())
            .then(()=>{
                return Promise.all([

                    fetch("/get_table?tp=" + "work_artices")//向后端发送读取work_artices文件中的数据的请求，并展示到前端
                        .then(res=>res.json())
                        .then(data=>{
                            data.forEach(item => {
                                $("#cngal_weekly_table").append(
                                    `<tr><td>${item.title}</td><td>${item.type}</td><td>${item.create_time}</td><td class="file_path">${item.maintext_path}</td><td><a href="${item.url}">${item.url}</a></td>`
                                )}
                            );
                        }),
                    
                    fetch("/add_sql")
                        .then(res=>res.json()
                        .then(data=>{return})
                    )
                    
                ])
            })
            .then(() => {
                setTimeout(() => {
                    autoScroll = false;
                }, 1500);  // 等 1.5 秒，确保最后一批日志被拉取
            data = null;
        });

        
        
    })
    //监控正文文件路径的点击，展示正文
    $("#cngal_weekly_table").on("click",".file_path",function(){

        var path = $(this).text().trim();  //获取本次点击的文本
        
        fetch("/get_maintext?path=" + path)  //向后端发起一个查找文件内容的请求
            .then(res=>res.text())
            .then(data=>{
                let cleanText = data.replace(/\\n/g, '\n');
                $("#file").text(cleanText)
                $("#show_table").css("width","50%")
                $("#show_file").show()
            })

    })
    //监控按钮：清空日志
    $("#clear_log").on("click",function(){
        let result = confirm("确定清空日志吗？（点击确定将清空下方日志，但不会删除日志文件，日志文件需手动清空；点击取消返回）")
        if(result){
            $(".log").remove()
        }else{

        }

    })
    //监控按钮：生成文件
    $("#get_excel").on("click", function () {
        let table = [];

        $("#cngal_weekly_table tbody tr").each(function () {
            let row = {};
            let $tds = $(this).find("td");

            row.title = $tds.eq(0).text().trim();
            row.type = $tds.eq(1).text().trim();
            row.create_time = $tds.eq(2).text().trim();
            row.maintext_path = $tds.eq(3).text().trim();
            row.url = $tds.eq(4).text().trim();

            table.push(row);
        });

        fetch("/get_excel", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(table)
        })
        .then(res => res.text())
        .then(data => {
            let w = confirm("文件保存成功，保存路径：" + data + "\n是否现在查看？");
            if (w) {
                fetch("/open_csv?path=" + data);
            }
        });
    });
    //监控按钮：下拉框
    var isOpen = false;
    $('#get').on('click', function () {
        isOpen = !isOpen;
        if (isOpen) {
            $('#more_conditions').show();
            $("#get").css("border-top","6px solid #ff1100")
        } else {
            $('#more_conditions').hide();
            $("#get").css("border-top","6px solid #0062ff")
        }
    });    
    //监控按钮：删除条件
    $('#all_userselect').on('click', 'button', function () {
        // 判断是不是删除按钮
        if ($(this).text().trim() === '删除') {
            // 找到它所在的那一条条件
            var $condition = $(this).closest('.user_select');
            $condition.remove();
        }
    });  
    //监控按钮：添加条件
    $("#add_condition").on('click',function(){
        var html = `
            <div class="user_select more-condition">
                <div class="choose_dbtype">
                    <select>
                        <option value="" disabled selected hidden>请选择查询类别</option>
                        <option>周报</option>
                        <option>游戏</option>
                        <option>文章</option>
                    </select>
                </div>
                <div class="choose_year">
                    <select>
                        <option value="" disabled selected hidden>请选择查询年份</option>
                        <option>2026</option>
                        <option>2025</option>
                        <option>2024</option>
                        <option>2023</option>
                        <option>2022</option>
                        <option>2021</option>
                    </select>
                </div>
                <div class="choose_month">
                    <select>
                        <option value="" disabled selected hidden>起始月份</option>
                        <option>12</option><option>11</option><option>10</option>
                        <option>9</option><option>8</option><option>7</option>
                        <option>6</option><option>5</option><option>4</option>
                        <option>3</option><option>2</option><option>1</option>
                    </select>
                    <p>-</p>
                    <select>
                        <option value="" disabled selected hidden>结束月份</option>
                        <option>12</option><option>11</option><option>10</option>
                        <option>9</option><option>8</option><option>7</option>
                        <option>6</option><option>5</option><option>4</option>
                        <option>3</option><option>2</option><option>1</option>
                    </select>
                </div>
                <div class="del">
                    <button class="btn-del">删除</button>
                </div>
            </div>
        `;
        $('#more_conditions').append(html);        
    })
    //监控按钮：重置筛选
    $("#reset_condition").on('click',function(){
        $('#more_conditions').empty();
    })
    //监控按钮：开始检索
    $("#select_db").on('click', function () {
        var conditions = [];

        $('#all_userselect .user_select').each(function () {
            var $s = $(this).find('select');
            var dbtype     = $s.eq(0).val() || "";
            var year       = $s.eq(1).val() || "";
            var monthStart = $s.eq(2).val() || "";
            var monthEnd   = $s.eq(3).val() || "";

            if (!dbtype && !year && !monthStart && !monthEnd) return;

            conditions.push({
                dbtype: dbtype,
                year: year,
                month_start: monthStart,
                month_end: monthEnd
            });
        });

        if (conditions.length === 0) {
            alert("请至少填写一个查询条件");
            return;
        }

        fetch("/select_history", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(conditions)
        })
        .then(res => res.json())
        .then(data => {
            $("#cngal_weekly_table tbody").empty();
            $("#show_table").show();

            data.forEach(item => {
                $("#cngal_weekly_table tbody").append(
                    `<tr>
                        <td>${item.title}</td>
                        <td>${item.type}</td>
                        <td>${item.create_time}</td>
                        <td class="file_path">${item.maintext_path}</td>
                        <td><a href="${item.url}">${item.url}</a></td>
                    </tr>`
                );
            });
        });
    });

})