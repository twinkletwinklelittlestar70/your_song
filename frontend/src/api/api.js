export const postMsg = (msg) => {
    return fetch('/api/send_msg', {
        body: JSON.stringify({message: msg}),
        headers: {
          'content-type': 'application/json'
        },
        method: 'POST',
      })
        .then((res) => {
            return res.json()
        })
        .catch(e => console.error(e))
}