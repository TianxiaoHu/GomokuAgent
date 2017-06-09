/* Copied and Modified from opensource project https://github.com/lihongxun945/gobang */
var Board = function(container, status) {
  this.container = container;
  this.status = status;
  this.step = this.container.width() * 0.065;
  this.offset = this.container.width() * 0.044;
  this.steps = [];

  this.started = false;
  this.container_x = container.offset().left;
  this.container_y = container.offset().top;

  var self = this;
  this.container.on("click", function(e) {
    if(self.lock || !self.started) return;
    var y = e.pageX - container.offset().left, x = e.pageY - container.offset().top;

    x = Math.floor((x+self.offset)/self.step) - 1;
    y = Math.floor((y+self.offset)/self.step) - 1;

    self.set_server(x, y)
  });


  this.setStatus("Welcome to Gomoku");

}



Board.prototype.start = function() {
  if(this.started) return;
  this.initBoard();
  this.draw();
  this.setStatus("Game Started!");
  this.started = true;
  this.playing = 2;
}

Board.prototype.stop = function() {
  if(!this.started) return;
  this.setStatus("Please Click Start");
  this.started = false;
}

Board.prototype.initBoard = function() {
  this.board = [];
  for(var i=0;i<15;i++) {
    var row = [];
    for(var j=0;j<15;j++) {
      row.push(0);
    }
    this.board.push(row);
  }
  this.steps = [];
}

Board.prototype.draw = function() {
  var container = this.container;
  var board = this.board;

  container.find(".chessman, .indicator").remove();

  for(var i=0;i<board.length;i++) {
    for(var j=0;j<board[i].length;j++) {
      if(board[i][j] != 0) {
        var chessman = $("<div class='chessman'></div>").appendTo(container);
        if(board[i][j] == 2) chessman.addClass("black");
        chessman.css("top", this.offset + i*this.step);
        chessman.css("left", this.offset + j*this.step);
      }
    }
  }

  if(this.steps.length > 0) {
    var lastStep = this.steps[this.steps.length-1];
    $("<div class='indicator'></div>")
      .appendTo(container)
      .css("top", this.offset + this.step * lastStep[0])
      .css("left", this.offset + this.step * lastStep[1])
  }

}


Board.prototype.setStatus = function(s) {
  this.status.text(s);
}

Board.prototype.set = function(x, y, role) {
  if(this.board[x][y] !== 0) {
    return;
  }
  // this.set_server(x,y);
  this.board[x][y] = role;
  this.steps.push([x,y]);
  this.draw();
  if(this.playing == 2) {this.playing = 1;}
  else if(this.playing == 1) {this.playing = 2;}
}

// Server functions passed to Flask
Board.prototype.set_server = function(x,y) {
  if(this.board[x][y] !== 0) {
    return;
  }
  this.set(x, y, this.playing)
  this.lock = true;
  var self = this;
  // console.log(this.board)
  // console.log(this.playing)
  var boardString = JSON.stringify(this.board);
  $.getJSON($SCRIPT_ROOT + '/_player_set', {position: x.toString() + ',' + y.toString(), board: boardString}, function(data) {
    //console.log(data);
    var ai_move = data.next_move;
    var winner = data.winner;
    if (ai_move !== null) {
      self.set(ai_move[0], ai_move[1], self.playing);
    }
    if (winner !== null) {
      $.alert(winner+" Win!", function() {self.stop();});
    }
    self.lock = false;
  });

};

var b = new Board($("#board"), $(".status"));
$("#start").click(function() {
  b.start();
});
