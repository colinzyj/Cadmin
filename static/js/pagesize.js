// 手动输入页码
function gotoPageNumberOnKeyDown(evt){
	evt = (evt) ? evt : ((window.event) ? window.event : "") //兼容IE和Firefox获得keyBoardEvent对象
	var key = evt.keyCode?evt.keyCode:evt.which; //兼容IE和Firefox获得keyBoardEvent对象的键值
    var gotoPageNum = document.getElementById("gotoPageNum").value;
    var pageNum = document.getElementById("pageNum").value;
    var maxPageNum = document.getElementById("maxPageNum").value;
	if (key == 13) {
		if (isNaN(gotoPageNum)){
		    document.getElementById("gotoPageNum").value =  1;
			return;
		}
        if (gotoPageNum%1 != 0) {
            document.getElementById("gotoPageNum").value =  gotoPageNum - gotoPageNum%1;
            return;
        }
	    if (( gotoPageNum <= 0 )|| ( gotoPageNum > maxPageNum )){
		  alert("页码范围有误");
		  return;
		}
		if(gotoPageNum==pageNum){
			alert("已是当前页");
			return ;
		}
		//document.query_form.pageNum.value = pageNum;
		//document.query_form.submit();
        gotoPage(gotoPageNum);
		return ;
	}
	return false;
}
//列排序
function sortby(col){
    if (col){
        document.query_form.query_sort.value = col;
        document.query_form.submit();
    };
}
//翻页
function gotoPage(pageNumber) {
	document.query_form.pageNum.value = pageNumber;
	document.query_form.submit();
}
//分页大小
function pageSizeChange(value){
	document.query_form.pageSize.value = value;
	document.query_form.submit();
}
// 动态调整表格宽度
var tTD; //用来存储当前更改宽度的Table Cell,避免快速移动鼠标的问题
var table = document.getElementById("tb_info"); //注意设置table id
for (j = 0; j < table.rows[0].cells.length; j++) {
    table.rows[0].cells[j].onmousedown = function () {
    //记录单元格
        tTD = this;
        if (event.offsetX > tTD.offsetWidth - 10) {
            tTD.mouseDown = true;
            tTD.oldX = event.x;
            tTD.oldWidth = tTD.offsetWidth;
        };
        //记录Table宽度
        //table = tTD; while (table.tagName != ‘TABLE') table = table.parentElement;
        //tTD.tableWidth = table.offsetWidth;
    };
    table.rows[0].cells[j].onmouseup = function () {
    //结束宽度调整
        if (tTD == undefined) tTD = this;
        tTD.mouseDown = false;
        tTD.style.cursor = 'default';
    };
    table.rows[0].cells[j].onmousemove = function () {
    //更改鼠标样式
        if (event.offsetX > this.offsetWidth - 10)
            this.style.cursor = 'col-resize';
        else
            this.style.cursor = 'default';
        //取出暂存的Table Cell
        if (tTD == undefined) tTD = this;
        //调整宽度
        if (tTD.mouseDown != null && tTD.mouseDown == true) {
            tTD.style.cursor = 'default';
            if (tTD.oldWidth + (event.x - tTD.oldX)>0)
                tTD.width = tTD.oldWidth + (event.x - tTD.oldX);
            //调整列宽
            tTD.style.width = tTD.width;
            tTD.style.cursor = 'col-resize';
            //调整该列中的每个Cell
            table = tTD; while (table.tagName != 'TABLE') table = table.parentElement;
            for (j = 0; j < table.rows.length; j++) {
                table.rows[j].cells[tTD.cellIndex].width = tTD.width;
            };
            //调整整个表
            //table.width = tTD.tableWidth + (tTD.offsetWidth – tTD.oldWidth);
            //table.style.width = table.width;
        };
    };
};
