function Zombies(table, error) {
  this.table = table;
  this.error = error;
  this.rows = table.getElementsByTagName('tbody')[0];
  this.sort = new Tablesort(table);
  this.timeout = null;
  // Clear the current error message
  this.signal('');
  //this.signal('The zombie outbreak is over, folks! Now go have a break\u2014you deserved it.');
  this.loop();
}

Zombies.prototype.loop = function() {
  var r = new XMLHttpRequest();
  r.onreadystatechange = function() {
    if (r.readyState === 4) {
      switch (r.status) {
        case 200:
          this.load(r.responseText);
        break;
        case 0:
          this.signal('Connection failed! Retrying...');
        break;
        case 404:
          this.signal('Could not find zombie data. Make sure the data collection script is running.');
        break;
        default:
          this.signal('Something went wrong! (Error ' + r.status + ')');
      }
      this.timeout = setTimeout(this.loop.bind(this), 2000);
    }
  }.bind(this);
  r.open('GET', 'cache.json', true);
  r.send(null);
};

Zombies.prototype.signal = function(message) {
  this.error.innerHTML = message;
  this.error.style.display = message ? 'block' : 'none';
}

Zombies.prototype.load = function(json) {
  var data = JSON.parse(json);
  // Clear existing rows
  while (this.rows.lastChild) {
    this.rows.removeChild(this.rows.lastChild);
  }
  // Add new data
  for (var k in data) {
    var tr = document.createElement('tr');
    var append = function(textOrElem) {
      var td = document.createElement('td');
      if (textOrElem === null || textOrElem === undefined) {
        td.appendChild(document.createTextNode('-'));
      } else if (typeof textOrElem === 'object') {
        td.appendChild(textOrElem);
      } else {
        td.appendChild(document.createTextNode(textOrElem));
      }
      tr.appendChild(td);
    };
    append((function () {
      // Link to the nation's info page
      var a = document.createElement('a');
      a.setAttribute('href', 'http://www.nationstates.net/nation=' + k);
      a.setAttribute('target', '_blank');
      a.appendChild(document.createTextNode(k));
      return a;
    })());
    var v = data[k] || {};
    append(v.action);
    append(v.survivors);
    append(v.zombies);
    append(v.dead);
    this.rows.appendChild(tr);
  }
  // Reload the interface
  this.sort.refresh();
  this.signal('');
};

window.addEventListener('load', function() {
  var table = document.getElementById('data');
  window.zombies = new Zombies(table, error);
}, false);
