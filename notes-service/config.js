require('dotenv').config();
console.log('Mongo URI:', process.env.MONGO_URI);

module.exports = {
    MONGO_URI: process.env.MONGO_URI,
    jwtSecret: process.env.JWT_SECRET_KEY
};


