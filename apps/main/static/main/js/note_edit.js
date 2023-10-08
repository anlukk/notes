var editing = false;

function editNote() {
    var noteTitle = document.getElementById('type-2');
    var editName = document.getElementById('editName');
    var editForm = document.getElementById('editForm');
    var editButton = document.getElementsByClassName('buttonSave')[0];

    editing = !editing;

    editButton.style.display = 'none';

    if (editing) {
        noteTitle.style.display = 'none';
        editName.style.display = 'block';
        editButton.innerText = 'Cancel';
        editForm.style.display = 'block';
    } else {
        noteTitle.style.display = 'block';
        editName.style.display = 'none';
        editButton.innerText = 'Edit';
        editForm.style.display = 'none';
    }
}

function saveNote() {
    var editName = document.getElementById('editName');
    var noteTitle = document.getElementById('noteTitle');
    var editForm = document.getElementById('editForm');
    noteTitle.innerText = editName.value;
    editNote();
}