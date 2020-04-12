require.config({
　paths: {
    "jquery": "jquery.min",
    "com": "common.min"
  }
});

require(['jquery','com'], function ($,com){
  //拼音索引显示/隐藏
  $('#J_Pinyin').on('click',function(){
    $('#J_PinyinLayer').toggle();
    $(document).one('click',function(){
      $('#J_PinyinLayer').hide();
    });
    return false;
  });
  $('#J_PinyinLayer').on('click',function(event){
    event.stopPropagation();
  });
  //关闭拼音索引
  $('#J_PinyinLayer').on('click','.close',function(){
    $('#J_PinyinLayer').hide();
  });
  //拼音索引切换
  $('#J_PinyinIdx').on('click','a',function(){
    var $this = $(this);
    if($this.hasClass('current'))return;
    var meter = $this.attr('data-letter');
    var url = '/ajax_api_index_pinyin?name=';
    var html = '';
    com.loadOpen();
    $.ajax({
      url:url+meter,
      type:'GET',
      timeout:10000,
      error:function(http,err){
        console.error(http,err);
        com.loadClose();
      },
      success:function(data){
        var json = JSON.parse(data);
        if(json.length > 0){
          $.each(json,function(i,e){
            html += '<li><a target="_blank" href="'+e.song_url+'">'+e.song_name+'</a></li>';
          });
          if(json.length>30){
            //html += '<li><a target="_blank" class="index_more" href="/list_0_img_1_000000.html">更多...</a></li>';
          }
          $('#J_PinyinData').find('ul').html(html);
          $this.addClass('current').siblings().removeClass('current');
        }
        com.loadClose();
      }
    });
  });
  //换一批功能
  $('#J_ChangeYouLikeBtn').on('click',function(){
    var jTab = $('#J_Tab');
    var curVal = jTab.find('.current').attr('data-cur');
    var url = '';
    switch(+curVal){
      case 0:
        url = '/ajax_api_index_change_like';
        break;
      case 1:
        url = '/ajax_api_index_change_new';
        break;
      case 2:
        url = '/ajax_api_index_change_singer';
        break;
      default:
        url = '/ajax_api_index_change_like';
    }
    com.loadOpen();
    $.ajax({
      url:url,
      type:'POST',
      timeout:10000,
      error:function(http,err){
        console.error(http,err);
        com.loadClose();
      },
      success:function(data){
        com.loadClose();
        var json = JSON.parse(data);
        var html = '';
        $.each(json,function(i,e){
          html += '<li>';
          if(curVal==2){
            html += '<a target="_blank" href="/singer-' + e.singer_id + '.html" '+
                    'title="歌手-' + e.singer_name + '" class="pic layz_load pic_po">' +
                    '<img data-src="' + e.artist_photo + '" alt="歌手' + e.singer_name + '的封面"></a>' +
                    '<h3><a target="_blank" href="/singer-' + e.singer_id + '.html" ' +
                    'title="歌手-' + e.singer_name + '">' + e.singer_name + '</a></h3>';
          }else{
            html += '<a target="play" href="/song_' + e.song_id + '.html" ' +
                    'class="pic layz_load pic_po" title="' + e.song_name + '-' + e.song_artist + '">' +
                    '<img data-src="' + e.song_image + '" alt="' + e.song_name + '的封面" ></a>' +
                    '<h3><a target="play" href="/song_' + e.song_id + '.html" ' +
                    'title="' + e.song_name + '-' + e.song_artist + '">' + e.song_name + '</a></h3>' +
                    '<div class="singer"><a target="_blank" href="singer-' + e.singer_id + '.html" ' +
                    'title="歌手-' + e.song_artist + '">' + e.song_artist + '</a></div>' +
                    '<div class="times">播放次数：<span>' + e.dynamic_play_count + '</span></div>';
          }
          html += '</li>';
        });
        $('#J_Tab_Con').find('.current').html(html);
        com.showImg();
      }
    });
  });
  //banner图切换
  new com.FocusSwitch($('#J_FocusSlider'),$('#J_FocusClick'),true,5000,$('#bannerLeftBtn'),$('#bannerRightBtn')).init();
  //楼层焦点切换
  $('.J_GoodsList').each(function(i,e){
    new com.FocusSwitch($(e),$(e).next()).init();
  });
  //楼层tab标签
  $('.J_RankTab').each(function(){
    com.tabSwitch($(this),$(this).next().find('.t_w'));
  });
  //猜您喜欢
  $('#J_ChangeYouLikeBtn').prop('title','猜您喜欢-换一批')
  com.tabSwitch($('#J_Tab'),$('#J_Tab_Con'),function(){
    $('#J_ChangeYouLikeBtn').prop('title',$('#J_Tab .current').text()+'-换一批')
  });
  //首页侧边导航滑过
  $('#J_CategoryDropdown').on({'mouseenter':function(){
      $('#J_CategoryDropdown').show();
    },'mouseleave':function(){
      $('#J_CategoryDropdown').hide();
      $('#J_CategoryItems').find('.hover').removeClass('hover');
    }
  });
  $('#J_CategoryItems').on({'mouseenter':function(){
      $('#J_CategoryDropdown').show().find('.category-all').eq($(this).index()).show().siblings().hide();
      $(this).addClass('hover').siblings().removeClass('hover');
    },'mouseleave':function(){
      $('#J_CategoryDropdown').hide();
      //$(this).removeClass('hover');
    }
  },'.item');
  $('#J_CategoryItems').on('mouseleave',function(){
    var _this = this;
    setTimeout(function(){
      if($('#J_CategoryDropdown').is(':hidden'))$(_this).find('.hover').removeClass('hover');
    });
  });
  $('.links').on('click','.down',function(){
    var $this = $(this);
    var url = '/ajax_api_index_song';
    var filter = $this.attr('data-filter');
    var orderby = $this.attr('data-orderby');
    com.loadOpen();
    $.ajax({
      url:url+'?filter_index='+filter+'&orderby_index='+orderby,
      type:'GET',
      timeout:10000,
      error:function(http,err){
        console.error(http,err);
        com.loadClose();
      },
      success:function(data){
        var json = JSON.parse(data);
        var ulArr = [];
        var ulList = $this.parent().parent().next().find('.content ul');
        var liStr = '';
        $.each(json,function(i,e){
          if(i != 0 && i%7 == 0){
            ulArr.push(liStr);
            liStr = '';
          }
          if(i%7 == 0){
            liStr += '<li class="first">';
          }else{
            liStr += '<li>';
          }
          liStr += '<a target="play" href="/song_' + e.song_id + '.html" class="pic layz_load pic_po">' +
                   '<img data-src="' + e.song_image + '"></a>' +
                   '<h3><a target="play" href="/song_' + e.song_id + '.html">' + e.song_name + '</a></h3>' +
                   '<div class="singer"><a target="_blank" href="/singer-' + e.artist_id + '.html">' + e.song_artist + '</a></div>' +
                   '<div class="times">播放次数：<span>' + e.dynamic_play_count + '</span></div>';
          if(i%7 == 0){
            liStr += '<div class="buttons"><a target="play" href="/song_' + e.song_id + '.html" class="buy-button">立即听听</a></div></li>';
          }else{
            liStr += '</li>';
          }
        });
        ulArr.push(liStr);
        if(ulArr.length > 0){
          $this.removeClass('down').siblings().addClass('down');
          $.each(ulList,function(i,e){
            if(ulArr[i]!=null)$(e).html(ulArr[i]);
          });
          com.showImg();
        }
        com.loadClose();
      }
    });
  });
});

let getRandomInt = (min, max) => {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
};

let mainHeart = anime();
let secondHeart = anime();

let path1 = anime.path('.line1');
let path2 = anime.path('.line2');
let path3 = anime.path('.line3');
let path4 = anime.path('.line4');
let path5 = anime.path('.line5');
let path6 = anime.path('.line6');
let path7 = anime.path('.line7');

let floatingHearts = () => {
    $('.heart').show();

    anime({ targets: '.heart1', translateX: path1('x'), translateY: path1('y'), scale: { value: [1, 0], delay: getRandomInt(400, 600), duration: getRandomInt(1000, 2000) }, easing: 'easeInOutCubic', duration: 2000 });
    anime({ targets: '.heart2', translateX: path2('x'), translateY: path2('y'), scale: { value: [1, 0], delay: getRandomInt(400, 600), duration: getRandomInt(1000, 2000) }, easing: 'easeInOutCubic', duration: 2000 });
    anime({ targets: '.heart3', translateX: path3('x'), translateY: path3('y'), scale: { value: [1, 0], delay: getRandomInt(400, 600), duration: getRandomInt(1000, 2000) }, easing: 'easeInOutCubic', duration: 2000 });
    anime({ targets: '.heart4', translateX: path4('x'), translateY: path4('y'), scale: { value: [1, 0], delay: getRandomInt(400, 600), duration: getRandomInt(1000, 2000) }, easing: 'easeInOutCubic', duration: 2000 });
    anime({ targets: '.heart5', translateX: path5('x'), translateY: path5('y'), scale: { value: [1, 0], delay: getRandomInt(400, 600), duration: getRandomInt(1000, 2000) }, easing: 'easeInOutCubic', duration: 2000 });
    anime({ targets: '.heart6', translateX: path6('x'), translateY: path6('y'), scale: { value: [1, 0], delay: getRandomInt(400, 600), duration: getRandomInt(1000, 2000) }, easing: 'easeInOutCubic', duration: 2000 });
    anime({ targets: '.heart7', translateX: path7('x'), translateY: path7('y'), scale: { value: [1, 0], delay: getRandomInt(400, 600), duration: getRandomInt(1000, 2000) }, easing: 'easeInOutCubic', duration: 2000 });
};

$('body').on('click', '.like', (e) => {
    let $this = $(e.currentTarget);

    if ($this.hasClass('active')) {
        secondHeart.pause();
        mainHeart.pause();
        $this.toggleClass('active');

        mainHeart = anime({ targets: '.like .main', scale: 1, duration: 1, delay: 0 });
        anime({ targets: '.like .second', scale: 0, easing: 'linear', duration: 150 });
    } else {
        secondHeart.pause();
        mainHeart.pause();
        $this.toggleClass('active');

        anime({
            targets: '.like .second',
            scale: 0,
            easeing: 'linear',
            duration: 0,
            complete: () => {
                secondHeart = anime({ targets: '.like .second', scale: 1 });
                mainHeart = anime({ targets: '.like .main', scale: 0, duration: 1, delay: 300 });
            }
        });

        floatingHearts();
    }
});