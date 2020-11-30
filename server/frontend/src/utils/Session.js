class Session {
    constructor(id, url, websocket, onReceive) {
        this.id = id
        this.url = url
        this.websocket = websocket
        this.onReceive = onReceive

        this.meta = null

        this.connect()
        .then(socket => {
            this.websocket = socket
            console.log("Successfully connected to Session")
        })
        .catch(error => {
            console.log("Error in connecting:", error)
        })
    }

    connect() {
        return new Promise((resolve, reject) => {
            const websocket = new WebSocket(this.url)
            
            websocket.onopen = () => {
                resolve(websocket)
            }
            websocket.onerror = error => {
                reject(error)
            }
            websocket.onmessage = event => {
                this.onReceive(event.data)
            }
        })
    }

    send() {
        if(this.websocket != null) {
            return new Promise((resolve, reject) => {
                this.websocket
            })
        } else {
            throw "No WebSocket connection detected."
        }
    }

    close() {

    }
}