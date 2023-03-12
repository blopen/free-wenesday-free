var record = false;
var actions = [];
var recordButton = document.createElement('button');
recordButton.innerHTML = 'Record';
recordButton.addEventListener('click', function() {
  record = true;
  actions = [];
});
document.body.appendChild(recordButton);
var stopButton = document.createElement('button');
stopButton.innerHTML = 'Stop';
stopButton.addEventListener('click', function() {
  record = false;
});
document.body.appendChild(stopButton);
var playButton = document.createElement('button');
playButton.innerHTML = 'Play';
playButton.addEventListener('click', function() {
  actions.forEach(function(action) {
    action();
  });
});
document.body.appendChild(playButton);
var doing = function(event) {
  if (record) {
    actions.push(function() {
      $(event.target).trigger(event.type);
      $(event.target).click().delay( 800 );
      console.log($(event.target).trigger(event.type))
    });
  }
};
document.addEventListener('click', doing);
document.addEventListener('keydown', doing);
document.addEventListener('keyup', doing);
var resetButton = document.createElement('button');
resetButton.innerHTML = 'Reset';
resetButton.addEventListener('click', function() {
  while (document.body.firstChild) {
    document.body.removeChild(document.body.firstChild);
  }
});
document.body.appendChild(resetButton);