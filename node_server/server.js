const express = require('express');
const serveIndex = require('serve-index');

const app = express();

app.use('/public', express.static('public'));
app.use('/public', serveIndex('public'));

app.get('/', (req, res) => {
  res.send('Successful response.');
});

const port = parseInt(process.env.PORT) || 8080;
app.listen(port, () => console.log('Example app is listening on port ${port}.'));