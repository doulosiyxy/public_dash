let dashCounter = 1;
let noOfGames = 15;

function isSafari() {
  return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
}

if (isSafari()) {
  /*function setHeightToWidth() {
    var containerWidth = $('.grid-container').width(); 
    var playerWidth = containerWidth / 12;
    $('.player').width(playerWidth); 
    $('.player').height(playerWidth);
  }
  setHeightToWidth();
  $(window).resize(function() {
    setHeightToWidth();
  });*/
}

$(document).ready(function () {
  //Event listeners

  $('.prev-btn').on('click', function () {
    getPrevious();
  });

  $('.swap-btn').on('click', function () {
    swap();
  });

  $('.next-btn').on('click', function () {
    getNext();
  });


  let adjustedLogo = ["Bears", "Dolphins", "Falcons", "Jaguars", "Lions", "Giants", "Buccaneers", "Panthers"]
  if (adjustedLogo.includes($('.def-name').attr('data-name'))) {
    $('.prediction-title-logo-one').css('margin-top', '30px');
  }
  else {
    $('.prediction-title-logo-one').css('margin-top', '0px');
  }

  if (adjustedLogo.includes($('.off-name').attr('data-name'))) {
    $('.prediction-title-logo-two').css('margin-top', '30px');
  } else {
    $('.prediction-title-logo-two').css('margin-top', '0px');
  }
  let x = $('.chart-percent-one').text().replace('%', "")
  let y = $('.chart-percent-two').text().replace('%', "")
  let colorOne = $('.diagram-team-def').css('background-color')
  let colorTwo = $('.diagram-team-off').css('background-color')
  /*$('.prediction-title-logo-one').css('background-color', colorOne)
  $('.prediction-title-logo-two').css('background-color', colorTwo)*/
  getChart(x, y, colorOne, colorTwo);
  $('.info-btn').on('click', info);
  $('.instructions').on('click', function () {
    $(this).addClass('alert-hide');
    $('.grid-container').toggleClass('disable');
  });
  $('.step').click((e) => {
    changePredicter(e);
  }
  );
});

function dashCount(num) {
  dashCounter = dashCounter + num;
}

function changeBtns() {
  switch (dashCounter) {
    case 1:
      $(".prev-btn").hide();
      $("#dash-btn-placeholder").show();
      break;
    case noOfGames:
      $(".next-btn").hide();
      $(".dash-btn-placeholder").show();
      break;
    default:
      $(".next-btn").css('display', 'flex');
      $(".prev-btn").css('display', 'flex');
      $("#dash-btn-placeholder").hide();
  }
}

function changeNav() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}

function changeHTML(response, call = "") {
  if (call != "swap") {
    let adjustedLogo = ["Bears", "Dolphins", "Falcons", "Jaguars", "Lions", "Giants", "Buccaneers", "Panthers"]
    if (adjustedLogo.includes(response.teamOne)) {
      $('.prediction-title-logo-one').css('margin-top', '30px');
    }
    else {
      $('.prediction-title-logo-one').css('margin-top', '0px');
    }

    if (adjustedLogo.includes(response.teamTwo)) {
      $('.prediction-title-logo-two').css('margin-top', '30px');
    } else {
      $('.prediction-title-logo-two').css('margin-top', '0px');
    }
    $('.week-no').text(response.week + ": " + response.game);
    $('.def-logo, .chart-logo-one, .table-logo-one, .prediction-title-logo-one').attr("src", response.teamOneLogo);
    $('.off-logo, .chart-logo-two, .table-logo-two, .prediction-title-logo-two').attr("src", response.teamTwoLogo);
    $('.table-ctw-one').text(response.teamOneCTW + "%");
    $('.table-ctw-two').text(response.teamTwoCTW + "%");
    $('.table-ctwd-one').text(response.teamOneCTWD + "%");
    $('.table-ctwd-two').text(response.teamTwoCTWD + "%");
    $('.table-w-one').text(response.teamOneW);
    $('.table-w-two').text(response.teamTwoW);
    $('.table-l-one').text(response.teamOneL);
    $('.table-l-two').text(response.teamTwoL);
    $('.standings-table').html(response.standingsHTML);
    $('.alert').html(response.alert);
    $('.news-wrapper').html(response.newsHTML).scrollTop(0);
    $("i[data-name]").attr('data-name', response.isSaved);
    if (response.weather) {
      $(".weather").html(response.weather.temp + "<sup>&deg;</sup>F")
      $(".wi").attr('class', 'wi wi-wu-' + response.weather.description.replace(/\/| /g, "").toLowerCase());
      $(".wi").attr('title', response.weather.description)
    } else {
      $(".weather").html("")
    }

  }
  $('.grid-container, .dash-btn-container').removeClass('disable');
  $('.def-logo').attr("src", response.teamOneLogo);
  $('.off-logo').attr("src", response.teamTwoLogo);
  $('.def-name').text(response.teamOne + " Defense");
  $('.off-name').text(response.teamTwo + " Offense");
  $('.offense').html(response.offHtml);
  $('.defense').html(response.defHtml);
  /*$('.offense-container').attr("onclick", "selectWinner('"+response.teamTwoId+"','"+response.teamTwo+"','"+response.teamTwoColor+"','"+response.gameid+"')");*/
  /*$('.defense-container').attr("onclick", "selectWinner('"+response.teamOneId+"','"+response.teamOne+"','"+response.teamOneColor+"','"+response.gameid+"')");*/
  $(".diagram-team-def").attr("style", "background-color: " + response.teamOneColor);
  $(".diagram-team-off").attr("style", "background-color: " + response.teamTwoColor);
  $('.instructions').addClass('alert-hide');
  if (isSafari()) {
    /*function setHeightToWidth() {
      var containerWidth = $('.grid-container').width(); 
      var playerWidth = containerWidth / 12;
      $('.player').width(playerWidth); 
      $('.player').height(playerWidth);
    }
    setHeightToWidth();
    $(window).resize(function() {
      setHeightToWidth();
    });*/
  }
}

function changeChart(response) {
  getChart(response.teamOneCTW, response.teamTwoCTW, response.teamOneColor, response.teamTwoColor)
  $('.chart-percent-one').html(response.teamOneCTW + "<sup>%</sup>")
  $('.chart-percent-two').html(response.teamTwoCTW + "<sup>%</sup>")
}

function changePredicter(e, reset = false) {
  if (reset) {
    setTimeout(5000);
    $('.predictor-table').hide();
    $('.chart-wrapper').show();
    $('.chart-btn').addClass("active");
    $('.table-btn').removeClass("active");
  } else {
    $(e.target).addClass("active");
    $(".step").not(e.target).removeClass("active");
    if ($(e.target).hasClass("chart-btn")) {
      $('.chart-wrapper').show();
      $('.predictor-table').hide();
    } else {
      $('.chart-wrapper').hide();
      $('.predictor-table').show();
    }
  }
}

function submitAlert() {
  $('.grid-container, .dash-btn-container').addClass('disable');
  $('.alert').removeClass('alert-hide');
  $('.cancel, .alert').on('click', () => {
    $('.alert').addClass('alert-hide');
    $('.grid-container, .dash-btn-container').removeClass('disable');
  });
  $('.undo').off('click').on('click', () => {
    $('.alert').addClass('alert-hide');
    $('.grid-container, .dash-btn-container').removeClass('disable');
  });
}

function selectWinner(teamId, teamName, color, gameId) {

  $('.grid-container, .dash-btn-container').addClass('disable');
  $('.alert img').attr('src', 'static/images/logo' + teamId + '.png');
  $('.alert p').text("Let's Go, " + teamName + "?")
  $('.alert').removeClass('alert-hide').css('background-color', color);
  $('.cancel, .alert').off('click').on('click', () => {
    $('.alert').addClass('alert-hide');
    $('.grid-container, .dash-btn-container').removeClass('disable');
  });
  $('.submit').off('click').on('click', () => {
    submitWinner(teamId, gameId, teamName);
    $('.alert').addClass('alert-hide');
    $('.grid-container, .dash-btn-container').removeClass('disable');
  });
}


function selectPlayer(event) {
  event.stopImmediatePropagation();
  alert("Player selected")
}

function info() {
  $('.instructions').toggleClass('alert-hide');
  $('.grid-container').toggleClass('disable');
}


/*ajax*/

function undo(gameId) {


  $.ajax({

    url: "/dashboard/undo",
    context: document.body,

    method: "POST",

    data: {

      gameId: gameId

    },

    success: function (response) {
      if (response) {
        /*console.log(response)*/
        $('.alert p').text(response).css('font-size', '1.2em');
        $('.feedback').html("<i class='fa fa-info-circle'></i><p>" + response + ".</p>").removeClass('alert-hide');
        setTimeout(function () {
          $('.feedback').addClass('alert-hide');
        }, 1000);
        refresh();
      }

    },

  });

}

function submitWinner(teamId, gameId, teamName) {


  $.ajax({

    url: "/dashboard/submitWinner",
    context: document.body,

    method: "POST",

    data: {

      teamId: teamId,
      gameId: gameId

    },

    success: function (response) {
      if (response) {
        /*console.log(response)*/
        $('.alert p').text(response).css('font-size', '1.2em');
        $('.feedback').html("<i class='fa fa-info-circle'></i><p>" + response + ".</p>").removeClass('alert-hide');
        setTimeout(function () {
          $('.feedback').addClass('alert-hide');
          if (dashCounter < noOfGames) {
            getNext();
          } else {
            refresh();
          }
        }, 2000);

      }

    },

  });

}


function refresh() {

  $.ajax({

    url: "/dashboard/refresh",
    context: document.body,

    method: "GET",

    data: {

    },

    success: function (response) {
      /*console.log(response)*/
      if (response) {
        changeHTML(response)
        changeChart(response)
        noOfGames = response.noOfGames
        changePredicter(null, true);
      }

    },

  });

}

function getNext() {
  $('.next-btn').attr('onclick', "");
  if (dashCounter < noOfGames) {
    dashCount(1);
    changeBtns();

    $.ajax({

      url: "/dashboard/getNext",
      context: document.body,

      method: "GET",

      data: {

      },

      success: function (response) {

        if (response) {
          changeHTML(response)
          changeChart(response)
          noOfGames = response.noOfGames
          changePredicter(null, true);
        }
        $('.next-btn').attr('onclick', "getNext()");

      },

    });

  }
}

function getPrevious() {
  $('.prev-btn').attr('onclick', "");
  if (dashCounter > 1) {

    dashCount(-1);
    changeBtns();


    $.ajax({

      url: "/dashboard/getPrev",
      context: document.body,

      method: "GET",

      data: {

      },

      success: function (response) {

        if (response) {
          changeHTML(response);
          changeChart(response);
          changePredicter(null, true);
        }
        $('.prev-btn').attr('onclick', "getPrevious()");

      },

    });

  }
}

function swap() {

  $.ajax({

    url: "/dashboard/swap",
    context: document.body,

    method: "GET",

    data: {

    },

    success: function (response) {
      changeHTML(response, "swap")
    },

  });
}


function getChart(valueOne, valueTwo, colorOne, colorTwo) {

  const predictorChart = document.getElementById('predictorChart');

  if (Chart.getChart(predictorChart)) {
    Chart.getChart(predictorChart)?.destroy()
  }

  const yValues = [valueOne, valueTwo];
  const barColors = [
    colorOne,
    colorTwo,
  ];

  new Chart(predictorChart, {
    type: "doughnut",
    data: {
      datasets: [{
        backgroundColor: barColors,
        data: yValues
      }]
    },

    options: {
      animation: false,
      tooltips: false,
      circumference: 360,
      radius: "70%",
      cutout: '70%',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          enabled: false
        },
        legend: {
          display: false
        }
      },
      hover: {
        mode: null
      }
    }
  });

}

/*main*/



