using UnityEngine;
using System.Collections;

public class Tile : MonoBehaviour {
   
    public Vector2 GridPosition = Vector2.zero;

    private Renderer rend;
    private Color defaultColor;

    // Use this for initialization
	void Start () {
        rend = GetComponent<Renderer>();
        defaultColor = rend.material.color;
    }
	
	// Update is called once per frame
	void Update () {
	
	}

    void OnMouseEnter()
    {
        if (GameManager.Instance.players[GameManager.Instance.PlayerIndex].moving)
        {
            rend.material.color = Color.blue;
        }
        else if (GameManager.Instance.players[GameManager.Instance.PlayerIndex].attacking)
        {
            rend.material.color = Color.red;
        }
    }
    void OnMouseExit()
    {
        rend.material.color = defaultColor;
    }
    void OnMouseDown()
    {
        if (GameManager.Instance.players[GameManager.Instance.PlayerIndex].moving)
        {
            GameManager.Instance.moveCurrentPlayer(this);
        }
        else if (GameManager.Instance.players[GameManager.Instance.PlayerIndex].attacking)
        {
            GameManager.Instance.attackWithCurrentPlayer(this);
        }
    }
}
