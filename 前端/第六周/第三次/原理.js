var timer = null,
    index = 0,
    pics = document.getElementsByClassName("banner-slide"),
    lis = document.getElementsByTagName("li");
 
 
//封装一个代替getElementById()的方法
function byId(id){
    return typeof(id) === "string"?document.getElementById(id):id;
}

function slideImg() {
    var main = byId("main");
    var banner = byId("banner");
    main.onmouseover = function(){
        stopAutoPlay();
    }
    main.onmouseout = function(){
        startAutoPlay();
    }
    main.onmouseout();
 
    //点击导航栏切换图片
    for(var i=0;i<pics.length;i++){
        lis[i].id = i;
          //给每个li项绑定点击事件
        lis[i].onclick = function(){
          //获取当前li项的index值
            index = this.id;
            changeImg();
        }
    }
}
//开始播放轮播图
function startAutoPlay(){
    timer = setInterval(function(){
        index++;
        if(index>3){
            index = 0;
        }
        changeImg();
    },1000);
}
//暂停播放
function stopAutoPlay(){
    if (timer) {
        clearInterval(timer);//定时器清零
    }
}
//改变轮播图
function changeImg(){
    for(var i=0;i<pics.length;i++){  //把非index全设置为不可见
        pics[i].style.display = "none";
        lis[i].className = "";
    }
    pics[index].style.display = "block"; //把当前index设为可见
    lis[index].className = "changeColor";//改变index的css
}
slideImg();

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>JS实现轮播图</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
    <div class="main" id="main">
        <div class="nav" id="nav">
            <ul>
                <li class="changeColor">首页</li>
                <li>点击看看</li>
                <li>会自动的</li>
                <li>我的网站</li>
            </ul>
        </div>
        <div class="banner" id="banner">
            <a href="#">
                <div class="banner-slide slide1"></div>
            </a>
            <a href="#">
                <div class="banner-slide slide2"></div>
            </a>
            <a href="#">
                <div class="banner-slide slide3"></div>
            </a>
            <a href="#">
                <div class="banner-slide slide4"></div>
            </a>
        </div>
    </div>
    <script type="text/javascript" src="js/script.js"></script>
</body>
</html>

* {
    padding: 0;
    margin: 0;
}
 
.main {
    width: 1200px;
    height: auto;
    margin: 50px auto;
    overflow: hidden;
}
 
.nav {
    width: 1200px;
    height: 80px;
}
 
ul {list-style-type: none;}
 
li {
    float: left;
    width: 25%;
    height: 80px;
    text-align: center;
    line-height: 80px;
    cursor: pointer;
}
 
.changeColor {
    background: #ffcc00;
    border-radius: 5px;
}
 
.banner {
    width: 1200px;
    height: 460px;
    overflow: hidden;
}
 
.banner-slide {
    width: 1200px;
    height: 460px;
    background-repeat: no-repeat;
    position: absolute;
}
 
.slide1 {
    background-image: url("../img/1.jpg");
}
.slide2 {
    background-image: url("../img/2.jpg");
}
.slide3 {
    background-image: url("../img/3.jpg");
}
.slide4 {
    background-image: url("../img/4.jpg");
}