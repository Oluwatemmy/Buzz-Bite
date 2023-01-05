function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`)
    // const likeButton = document.getElementById(`likes-button-$(postId)`)

    fetch (`/like-post/${postId}`, {method: "POST"})
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            console.log(data)
        })
        .catch((e) => {
            console.log(e);
            alert("Could not like post.")
        });
}
