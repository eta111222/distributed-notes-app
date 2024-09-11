const express = require('express');
const mongoose = require('mongoose');
const config = require('../config');
const routes = require('./routes');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

mongoose.connect(config.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
})
.then(() => console.log('MongoDB connected'))
.catch((err) => console.log(err));

app.get('/', (req, res) => {
    res.send('Welcome to the Notes Service API!');
});

app.use('/api/notes', routes);

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
