console.log("Hello World")

const eventBox = document.getElementById("event-box")
const countdownBox = document.getElementById("countdown-box")
const dow = document.getElementsByClassName("lll")

console.log(eventBox.textContent)

const eventDate = Date.parse(eventBox.textContent)
console.log(eventDate)

const myCountDown = setInterval(()=>{
    const now = new Date().getTime()

    const diff = eventDate - now

    const d = Math.floor(eventDate / (1000 * 60 * 60 * 24) - (now / (1000 * 60 * 60 * 24)))
    const h = Math.floor((eventDate / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24)
    const m = Math.floor((eventDate / (1000 * 60) - (now / (1000 * 60))) % 60)
    const s = Math.floor((eventDate / (1000) - (now / (1000))) % 60)

    if (diff>0) {
        countdownBox.textContent = d + " days, " + h + " hours, " + m + " minutes, " + s + " seconds"
    } else {
        countdownBox.textContent = "It is time for the match"
    }

}, 1000)