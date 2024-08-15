import mongoose, { Schema } from 'mongoose';

// Schema definition for the Task  
const taskSchema: Schema = new Schema({  
    category: { type: String, required: true },  
    title: { type: String, required: true },  
    description: { type: String, required: true },  
    reward: { type: Number, required: true },  
});  

// Create and export the model compiled from the schema  
const Task = mongoose.model('Task', taskSchema);  

export default Task;