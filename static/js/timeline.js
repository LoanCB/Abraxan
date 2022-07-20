let steps = document.querySelector("#steps")
let tickIcon = `
<svg viewBox="0 0 512 512" width="100" title="check">
    <path d="M173.898 439.404l-166.4-166.4c-9.997-9.997-9.997-26.206 0-36.204l36.203-36.204c9.997-9.998 26.207-9.998 36.204 0L192 312.69 432.095 72.596c9.997-9.997 26.207-9.997 36.204 0l36.203 36.204c9.997 9.997 9.997 26.206 0 36.204l-294.4 294.401c-9.998 9.997-26.207 9.997-36.204-.001z"></path>
</svg>
`

steps.innerHTML = wizards
    .map(function (wizard) {
        return (
            `<div class='step'>` +
                `<div class='number ${wizard.complete && 'completed'}'>` +
                    (wizard.complete ? tickIcon : wizard.number) +
                `</div>` +
                `<div class='info'>` +
                    `<p class='title'>${wizard.title}</p>` +
                    `<p class='text'>${wizard.text ? wizard.text : ''}</p>` +
                "</div>" +
            "</div>"
        )
    })
    .join("")
