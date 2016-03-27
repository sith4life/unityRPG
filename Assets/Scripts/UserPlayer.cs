using UnityEngine;
using System.Collections;

public class UserPlayer : Player
{
    public float moveSpeed;
    Renderer rend;
	
    // Use this for initialization
	void Start () {
        moveSpeed = 10.0f;
        rend = gameObject.GetComponent<Renderer>();
    }
	
	// Update is called once per frame
	void Update () {
        if (GameManager.Instance.players[GameManager.Instance.PlayerIndex] == this) // is this (the current) player referenced in the GameManager
        {
            rend.material.color = Color.yellow;
        }
        else
        {
            rend.material.color = Color.white;
        }
        if (HP <= 0)
        {
            transform.rotation = Quaternion.Euler(new Vector3(transform.rotation.eulerAngles.x + 90, transform.rotation.eulerAngles.x, transform.rotation.eulerAngles.x));
            rend.material.color = Color.red;
        }
    }
    public override void TurnUpdate()
    {
        if (Vector3.Distance(moveDestination,transform.position) > 0.1f)
        {
            transform.position += (moveDestination - transform.position).normalized * moveSpeed * Time.deltaTime;
            if (Vector3.Distance(moveDestination, transform.position) <= 0.1f)
            {
                transform.position = moveDestination;
                ActionPoints--;
            }
        }
        base.TurnUpdate();
    }
    public override void TurnOnGUI()
    {
        float buttonHeight = 50;
        float buttonWidth = 90;
        
        // move button
        if (GUI.Button(new Rect(0, Screen.height - buttonHeight * 3, buttonWidth, buttonHeight), "Move"))
        {
            moving = !moving;
            attacking = false;
        }

        // attack button
        if (GUI.Button(new Rect(0, Screen.height - buttonHeight * 2, buttonWidth, buttonHeight), "Attack"))
        {
            moving = false;
            attacking = !attacking;
        }

        // end turn button
        if (GUI.Button(new Rect(0, Screen.height - buttonHeight * 1, buttonWidth, buttonHeight), "End Turn"))
        {
            ActionPoints = 2;
            moving = false;
            attacking = false;
            GameManager.Instance.NextTurn();
        }

        base.TurnOnGUI();
    }

    

}
