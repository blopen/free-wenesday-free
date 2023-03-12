var actions = [];
var seconds = 0;
var start = prompt("Do you want to start recording actions?");
if (start == "y") {
    startTime = new Date();
    endTime = new Date();
    timeDiff = endTime - startTime; //in ms
    //in seconds
    timeDiff /= 1000;
    seconds = Math.round(timeDiff);
    interval = setInterval(function () {
        if (seconds == 60) {
            clearInterval(interval);
        }
    }, 1000);
    var interval = setInterval(function () {
        if (seconds == 60) {
            clearInterval(interval);
            var repeat = prompt("Do you want to repeat recording actions?");
            if (repeat == "yes") {
                startTime = new Date();
                endTime = new Date();
                timeDiff = endTime - startTime; //in ms
                //in seconds
                timeDiff /= 1000;
                seconds = Math.round(timeDiff);
                interval = setInterval(function () {
                    if (seconds == 60) {
                        clearInterval(interval);
                    }
                }, 1000);
            }
        }
    }, 1000);
    document.addEventListener('click', function (e) {
        actions.push({
            type: 'click',
            x: e.clientX,
            y: e.clientY
        });
    });
    document.addEventListener('keydown', function (e) {
        actions.push({
            type: 'keydown',
            key: e.key
        });
    });
}
