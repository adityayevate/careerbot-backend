from flask import Flask, request, jsonify
import requests
import random
import os  # Import os to read environment variables

app = Flask(__name__)

# Sample list of career tips
career_tips = [
    "🌟 Keep learning new skills—online courses can boost your resume!",
    "🧠 Network with professionals in your field on LinkedIn regularly.",
    "📄 Tailor your resume for each job you apply to—it really makes a difference!",
    "🎯 Set short-term and long-term career goals and track your progress.",
    "💬 Practice your communication skills—they’re just as important as technical skills!",
    "🔍 Stay updated with trends and technologies in your industry.",
    "👔 Dress professionally for interviews—even virtual ones!",
]

# Sample list for appointment slots (could be dynamically fetched from a calendar)
appointment_slots = [
    "Monday at 10 AM",
    "Tuesday at 2 PM",
    "Wednesday at 11 AM",
    "Thursday at 1 PM",
    "Friday at 9 AM",
]

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    intent = data["queryResult"]["intent"]["displayName"]

    if intent == "FindJobIntent":
        job_title = data["queryResult"]["parameters"].get("job_title", "")
        location = data["queryResult"]["parameters"].get("geo-city", "")

        if job_title and location:
            # Adzuna API credentials
            app_id = "3530f725"
            api_key = "8929c9f89b930c2983e543ab01231472"
            url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={app_id}&app_key={api_key}&results_per_page=5&what={job_title}&where={location}"

            response = requests.get(url)

            if response.status_code == 200:
                job_data = response.json()
                jobs = job_data.get("results", [])

                if jobs:
                    job_list = "\n".join([f"🔹 {job['title']} at {job['company']['display_name']}" for job in jobs])
                    return jsonify({
                        "fulfillmentText": f"Here are some {job_title} jobs in {location}:\n{job_list}"
                    })
                else:
                    return jsonify({
                        "fulfillmentText": f"Sorry, I couldn't find any {job_title} jobs in {location}."
                    })
            else:
                return jsonify({
                    "fulfillmentText": "Hmm, I couldn’t fetch job listings right now. Try again soon!"
                })
        else:
            return jsonify({
                "fulfillmentText": "Please provide both a job title and location to find job listings."
            })

    elif intent == "CareerTipIntent":
        tip = random.choice(career_tips)
        return jsonify({
            "fulfillmentText": f"💡 Career Tip: {tip}"
        })

    elif intent == "BookCounselingIntent":
        # This intent handles booking career counseling appointments.
        # Asking for a preferred time slot
        return jsonify({
            "fulfillmentText": f"Please choose a time slot for your career counseling appointment:\n" + "\n".join(appointment_slots)
        })

    elif intent == "BookCounselingFollowUpIntent":
        # User selects a time slot (handle this part)
        chosen_slot = data["queryResult"]["parameters"].get("time_slot", "")
        if chosen_slot:
            return jsonify({
                "fulfillmentText": f"Your career counseling appointment has been scheduled for {chosen_slot}. Looking forward to helping you!"
            })
        else:
            return jsonify({
                "fulfillmentText": "Please select a valid time slot from the options."
            })

    else:
        return jsonify({
            "fulfillmentText": "I'm not sure how to help with that. Try asking for job listings, a career tip, or a counseling appointment!"
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use the environment variable for port
    app.run(host="0.0.0.0", port=port)  # Listen on all interfaces, Render assigns a dynamic port
