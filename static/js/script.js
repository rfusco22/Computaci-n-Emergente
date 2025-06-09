class TouristChatbot {
  constructor() {
    this.messageInput = document.getElementById("messageInput")
    this.sendButton = document.getElementById("sendButton")
    this.chatMessages = document.getElementById("chatMessages")
    this.loading = document.getElementById("loading")
    this.charCount = document.getElementById("charCount")

    this.initializeEventListeners()
    this.updateCharCount()
  }

  initializeEventListeners() {
    // Send message on Enter key
    this.messageInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault()
        this.sendMessage()
      }
    })

    // Character count update
    this.messageInput.addEventListener("input", () => {
      this.updateCharCount()
    })

    // Send button click
    this.sendButton.addEventListener("click", () => {
      this.sendMessage()
    })
  }

  updateCharCount() {
    const count = this.messageInput.value.length
    this.charCount.textContent = count

    if (count > 450) {
      this.charCount.style.color = "#ef4444"
    } else if (count > 400) {
      this.charCount.style.color = "#f59e0b"
    } else {
      this.charCount.style.color = "#6b7280"
    }
  }

  async sendMessage() {
    const message = this.messageInput.value.trim()

    if (!message) return

    // Disable input while processing
    this.setInputState(false)

    // Add user message to chat
    this.addMessage(message, "user")

    // Clear input
    this.messageInput.value = ""
    this.updateCharCount()

    // Show loading
    this.showLoading(true)

    try {
      // Send message to backend
      const response = await fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message }),
      })

      const data = await response.json()

      // Hide loading
      this.showLoading(false)

      // Add bot response
      this.addMessage(data.response, "bot")
    } catch (error) {
      console.error("Error:", error)
      this.showLoading(false)
      this.addMessage("Lo siento, hubo un error. Por favor, intenta de nuevo.", "bot")
    } finally {
      // Re-enable input
      this.setInputState(true)
    }
  }

  addMessage(text, sender) {
    const messageDiv = document.createElement("div")
    messageDiv.className = `message ${sender}-message`

    const avatar = document.createElement("div")
    avatar.className = "message-avatar"
    avatar.innerHTML = sender === "bot" ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>'

    const content = document.createElement("div")
    content.className = "message-content"

    const paragraph = document.createElement("p")
    paragraph.textContent = text
    content.appendChild(paragraph)

    messageDiv.appendChild(avatar)
    messageDiv.appendChild(content)

    this.chatMessages.appendChild(messageDiv)
    this.scrollToBottom()
  }

  setInputState(enabled) {
    this.messageInput.disabled = !enabled
    this.sendButton.disabled = !enabled

    if (enabled) {
      this.messageInput.focus()
    }
  }

  showLoading(show) {
    this.loading.style.display = show ? "flex" : "none"
    if (show) {
      this.scrollToBottom()
    }
  }

  scrollToBottom() {
    setTimeout(() => {
      this.chatMessages.scrollTop = this.chatMessages.scrollHeight
    }, 100)
  }

  clearChat() {
    // Keep only the initial bot message
    const messages = this.chatMessages.querySelectorAll(".message")
    for (let i = 1; i < messages.length; i++) {
      messages[i].remove()
    }
  }
}

// Quick message function
function sendQuickMessage(message) {
  const chatbot = window.chatbotInstance
  chatbot.messageInput.value = message
  chatbot.sendMessage()
}

// Clear chat function
function clearChat() {
  if (confirm("¿Estás seguro de que quieres limpiar el chat?")) {
    window.chatbotInstance.clearChat()
  }
}

// Initialize chatbot when page loads
document.addEventListener("DOMContentLoaded", () => {
  window.chatbotInstance = new TouristChatbot()
})

// Add some interactive features
document.addEventListener("DOMContentLoaded", () => {
  // Add typing indicator
  let typingTimeout

  document.getElementById("messageInput").addEventListener("input", () => {
    clearTimeout(typingTimeout)

    // Show typing indicator after user stops typing for 2 seconds
    typingTimeout = setTimeout(() => {
      // Could add typing indicator here if needed
    }, 2000)
  })

  // Add smooth scrolling behavior
  const chatMessages = document.getElementById("chatMessages")
  chatMessages.style.scrollBehavior = "smooth"
})
