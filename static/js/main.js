/**
* Create a popup notification with a message
* @param text the message to display
* @param type can be 'success', 'error', 'notice', 'info'
*/
function notification(text, type = 'success') {
    // Add default text based on the type if not provided
    if (text === undefined) {
        if (type === 'success') {
            text = 'Modifications enregistrées !'
        } else if (type === 'error') {
            text = "Une erreur s'est produite. Vous n'avez probablement pas les droits d'effectuer cette action."
        } else {
            console.error('No text was given for the notification...')
            return
        }
    }

    // show notification
    const flashes = document.getElementById('messages-section')
    flashes.innerHTML += `
<div class="flash flash-${type}">
    <div class="close">
        <i class="fa-solid fa-xmark" onclick="close_notification(this)"></i>
    </div>
    <span>${text}</span>
</div>
    `
}