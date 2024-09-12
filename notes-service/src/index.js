const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const config = require('../config');
const routes = require('./routes');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(cors());

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

app.listen(port, '0.0.0.0',() => {
    console.log(`Server running on http://localhost:${port}`);
    console.log(`Loaded JWT_SECRET_KEY: ${process.env.JWT_SECRET_KEY}`);
});
