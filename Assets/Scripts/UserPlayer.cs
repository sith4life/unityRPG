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
    public override void Update () {
        if (GameManager.Instance.players[GameManager.Instance.PlayerIndex] == this) // is this (the current) player referenced in the GameManager
        {
            rend.material.color = Color.yellow;
        }
        else
        {
            rend.material.color = Color.white;
        }
        base.Update();
    }
    public override void TurnUpdate()
    {
        if (positionQueue.Count > 0)
        {
            if (Vector3.Distance(positionQueue[0], transform.position) > 0.1f)
            {
                transform.position += (positionQueue[0] - transform.position).normalized * moveSpeed * Time.deltaTime;
            }
            if (Vector3.Distance(positionQueue[0], transform.position) <= 0.1f)
            {
                transform.position = positionQueue[0];
                positionQueue.RemoveAt(0);
                if (positionQueue.Count == 0)
                {
                    actionPoints--;
                }
            }
        }
        base.TurnUpdate();
    }
    public override void TurnOnGUI()
    {
        // diffs below

        if (!moving)
        {
            GameManager.Instance.RemoveTileHightlights();
            moving = !moving;
            attacking = false;
            GameManager.Instance.hightlightTilesAt(GridPosition, Color.blue, movementRange, false);
        }
        else
        {
            attacking = false;
            moving = false;
            GameManager.Instance.RemoveTileHightlights();
        }

        if (!attacking)
        {
            moving = false;
            attacking = !attacking;
            GameManager.Instance.hightlightTilesAt(GridPosition, Color.red, attackRange);
        }
        else
        {
            moving = false;
            attacking = false;
            GameManager.Instance.RemoveTileHightlights();
        }

        // EndTurnButton add 
        GameManager.Instance.RemoveTileHightlights();
    }
}
