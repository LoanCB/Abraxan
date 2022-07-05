const boxFlashes = document.querySelectorAll(".flashes .flash")

boxFlashes.forEach(box => {
    box.onclick = () => {close(box)}
    box.querySelector(".close").onclick = () => {close(box)}
})

let close = (box) => {
    box.style.transform = "translateX(calc(100% + 15px))"
    setTimeout(() => {
        box.remove()
    }, 300)
}

function close_notification(element) {
    element.parentNode.parentNode.parentNode.removeChild(element.parentNode.parentNode)
}