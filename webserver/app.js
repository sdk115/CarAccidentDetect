const PORT = 10002;
const express = require('express');
const Request = require('request');

let app = express();
let DB = require('mysql').createConnection({
    host: "gomguk.com",
    port: 13306,
    user: "root",
    password: "dbmaster",
    database: "sensor"
});
let util = require('util')
app.locals.pretty = true;
app.set('view engine', 'jade');
app.set('views', './views');
app.use(express.static('public'));



function page(req, res, layout, data) {

		if(req.query.lang) req.session.lang = req.query.lang;
    res.render(`layouts/${layout}`, Object.assign({
        page: layout,
    }, data));
}
app.get('/', function (req, res) {
    page(req,res, "index")
});

app.get('/insert/value', function (req, res) {
    let source = req.query.source
    let type = req.query.type
    let value = req.query.value

    let insert_query = "INSERT INTO sensor_value (source, type, value) values (%s, %s, %s)"
    DB.query(util.format(insert_query, source, type, value), (err, doc) => {
        if(err) console.warn(err.toString());
        else console.log('1 row is inserted');

    });
    res.send(source + type + value);
});

app.get('/distance/accident', function (req, res) {
    let lat = req.query.lat
    let lng = req.query.lng

    res.send(lat +"/" +lng);
});

app.listen(PORT, function () {
    console.log('app listening on port '+PORT)
});
