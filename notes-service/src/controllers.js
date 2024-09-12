const Note = require('./models');

exports.createNote = async (req, res) => {
    const { title, content, user } = req.body;

    try {
        const newNote = new Note({
            title,
            content,
            user
        });
        console.log('Creating new note:', newNote);

        const savedNote = await newNote.save();
        console.log('Note successfully saved:', savedNote);

        return savedNote;
    } catch (err) {
        res.status(500).json({ message: 'Error creating note' });
    }
};

exports.getNotes = async (req, res) => {
    const user = req.user;    
    try {
        const notes = await Note.find({ user });
        res.json(notes);
    } catch (err) {
        res.status(500).json({ message: 'Error fetching notes' });
    }
};

exports.getNoteById = async (req, res) => {
    try {
        const note = await Note.findById(req.params.id);
        if (!note) return res.status(404).json({ message: 'Note not found' });
        res.json(note);
    } catch (err) {
        res.status(500).json({ message: 'Error fetching note' });
    }
};

exports.updateNote = async (noteId, noteData) => {
    try {
        const updatedNote = await Note.findByIdAndUpdate(noteId, noteData, { new: true });
        return updatedNote;
    } catch (err) {
        throw new Error('Error updating note');
    }
};


exports.deleteNote = async (req, res) => {
    try {
        await Note.findByIdAndDelete(req.params.id);
        res.json({ message: 'Note deleted' });
    } catch (err) {
        res.status(500).json({ message: 'Error deleting note' });
    }
};
