//获取用户输入数据
function getFormData() {
  data = {
    choose_source: $choose_source.find("option:selected").text().trim(),
    choose_cngal_type: $choose_cngal_type.find("option:selected").text().trim(),
    choose_cngal_second_type: $choose_cngal_second_type.find("option:selected").text().trim(),
    year:$choose_year.find("option:selected").text().trim(),
    page_start: parseInt($start_page.val()),
    page_end: parseInt($end_page.val())
  };
  if (!data.choose_source || !data.choose_cngal_type ||
      !data.choose_cngal_second_type || !data.year ||
      isNaN(data.page_start) || isNaN(data.page_end)) {
      return null;   // 返回 null 表示数据不完整
  }
  return data
}
//获取用户选择的数据源的数据
function show_filter_criteria(choose_source){
    
  if(choose_source=="cngal网站"){
    $choose_cngal_type.show()
  }

}
//获取用户选择的要爬取的数据类型的数据
function show_choose_week_year(choose_type){
        
    if(choose_type=="文章"){
        $choose_condition_a.show()
        $choose_condition_b.show()
        $choose_condition_c.show()
    }
}
