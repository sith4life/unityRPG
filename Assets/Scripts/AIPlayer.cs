using UnityEngine;
using System.Collections;

public class AIPlayer : Player
{
    public float moveSpeed;
	// Use this for initialization
	void Start () {
        moveSpeed = 10f;
    }
	
	// Update is called once per frame
	void Update () {

    }

    public override void TurnUpdate()
    {
        if (Vector3.Distance(moveDestination, transform.position) > 0.1f)
        {
            transform.position += (moveDestination - transform.position).normalized * moveSpeed * Time.deltaTime;
            if (Vector3.Distance(moveDestination, transform.position) <= 0.1f)
            {
                transform.position = moveDestination;
                ActionPoints--;
            }
        }
        else
        {
            // add fight em logix here
            moveDestination = new Vector3(0 - Mathf.Floor(GameManager.Instance.MapSize / 2), 1.5f, -0 + Mathf.Floor(GameManager.Instance.MapSize / 2));
        }
        base.TurnUpdate();
    }
    public override void TurnOnGUI()
    {
        base.TurnOnGUI();
    }
}
