import cvxpy as cp
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Define activities and their effect on life factors
activities = {
    "work": {"happiness": -2, "health": -1, "career": 10, "relationships": -3, "personalGrowth": 2},
    "exercise": {"happiness": 5, "health": 10, "career": 0, "relationships": 0, "personalGrowth": 3},
    "socialize": {"happiness": 8, "health": 2, "career": 0, "relationships": 10, "personalGrowth": 1},
    "relax": {"happiness": 10, "health": 5, "career": 0, "relationships": 5, "personalGrowth": 2},
}

@app.post("/api/optimize_qp")
async def optimize_qp(request: Request):
    data = await request.json()
    hours_available = data.get("hours_available", 168)

    # Variables for hours allocated to each activity
    hours = cp.Variable(len(activities), nonneg=True)

    # Objective: Minimize variance (imbalances) and maximize total score
    factors = ["happiness", "health", "career", "relationships", "personalGrowth"]
    activity_matrix = [
        [activities[activity][factor] for factor in factors]
        for activity in activities
    ]
    scores = cp.matmul(activity_matrix, hours)

    # Minimize the variance between factors while maximizing total scores
    objective = cp.Minimize(cp.norm(scores - cp.mean(scores)) - cp.sum(scores))

    # Constraints: Total time and non-negative allocation
    constraints = [cp.sum(hours) == hours_available]

    # Solve the optimization
    problem = cp.Problem(objective, constraints)
    problem.solve()

    if problem.status == cp.OPTIMAL:
        allocation = {activity: hours.value[i] for i, activity in enumerate(activities)}
        scores_result = {factors[i]: scores.value[i] for i in range(len(factors))}
        return JSONResponse({"success": True, "allocation": allocation, "scores": scores_result})
    else:
        return JSONResponse({"success": False, "message": "Optimization failed"})
