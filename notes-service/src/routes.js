const express = require('express');
const { createNote, getNotes, getNoteById, updateNote, deleteNote } = require('./controllers');
const { authenticateJWT } = require('./middleware');
const amqp = require('amqplib/callback_api');
const axios = require('axios');

const router = express.Router();

const verifyUser = async (token) => {
    try {
        const response = await axios.get('http://user-service:5000/auth/api/verify', {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (err) {
        console.error('User verification failed:', err.response ? err.response.data : err.message);
        throw new Error('User verification failed');
    }
};

function publishNoteEvent(eventType, note) {
    try {
        amqp.connect('amqp://rabbitmq:5672', (err, connection) => {
            if (err) throw err;

            connection.createChannel((err, channel) => {
                if (err) throw err;

                const exchange = 'note_events';
                const message = JSON.stringify({ eventType, note });

                channel.assertExchange(exchange, 'fanout', { durable: false });

                channel.publish(exchange, '', Buffer.from(message));
                console.log(`[x] Sent ${eventType} event: ${message}`);

                setTimeout(() => {
                    connection.close();
                }, 500);
            });
        });
    } catch (err) {
        console.error('Error publishing event:', err);
    }
}


router.post('/', authenticateJWT, async(req, res, next) => {
    const { authorization } = req.headers;  

    if (!authorization || !authorization.startsWith('Bearer ')) {
        return res.status(401).json({ message: 'Authorization header missing or malformed' });
    }

    const token = authorization.split(' ')[1];  
    console.log(`Token being sent for verification: ${token}`);  

    try {
        const user = await verifyUser(token);

        const savedNote = await createNote(req, res);

        console.log('Note successfully saved:', savedNote);

        if (savedNote) {
            console.log('Note successfully saved:', savedNote);
            publishNoteEvent('note_created', savedNote);
            return res.status(201).json(savedNote);
        } else {
            return res.status(400).json({ message: 'Error saving note' });
        }
    } catch (err) {
        if (!res.headersSent) {
            res.status(500).json({ message: err.message });
        }
    }
});


router.put('/:id', authenticateJWT, async(req, res, next) => {
    const { authorization } = req.headers;
    const token = authorization.split(' ')[1];

    try {
        const user = await verifyUser(token);

        const updatedNote = await updateNote(req.params.id, req.body);

        console.log('Updated note:', updatedNote);

        if (updatedNote) {
            console.log('Updated note:', updatedNote);
            publishNoteEvent('note_updated', updatedNote);
            return res.status(200).json(updatedNote);
        } else {
            return res.status(404).json({ message: 'Note not found' });
        }  
    } catch (err) {
        if (!res.headersSent) {
            res.status(500).json({ message: err.message });
        }
    }
});

router.delete('/:id', authenticateJWT, async (req, res, next) => {
    const { authorization } = req.headers;
    const token = authorization.split(' ')[1];

    try {
        const user = await verifyUser(token);

        const deletedNote = await deleteNote(req, res);
        if (deletedNote) {
            console.log('Note successfully deleted:', deletedNote);

            publishNoteEvent('note_deleted', deletedNote);

            return res.status(200).json({ message: 'Note deleted', deletedNote });
        } else {
            return res.status(404).json({ message: 'Note not found' });
        }
    } catch (err) {
        if (!res.headersSent) {
            res.status(500).json({ message: err.message });
        }
    }
});

router.get('/', authenticateJWT, getNotes);
router.get('/:id', authenticateJWT, getNoteById);


module.exports = router;
