// improve this code
var actions = [];
document.addEventListener('click', function(e) {
  if (new Date() - startTime < 60000) {
    lastAction.innerHTML = 'Last action: ' + e.type + ' at ' + e.pageX + ', ' + e.pageY;
    actions.push({
      type: e.type,
      pageX: e.pageX,
      pageY: e.pageY
    });
  }
});
var repeat = prompt('Finished recording. How many times would you like to repeat the recorded actions?');
for (var i = 0; i < repeat; i++) {
  for (var j = 0; j < actions.length; j++) {
    var action = actions[j];
    var event = new MouseEvent(action.type, {
      pageX: action.pageX,
      pageY: action.pageY
    });
    document.dispatchEvent(event);
  }
}
// python3 hallo welt example