using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class Tile : MonoBehaviour {
   
    public Vector2 GridPosition = Vector2.zero;
    List<Tile> neighbours = new List<Tile>();
    public int movementCost = 1;
    public bool imPassable = false;

    private Renderer rend;
    private Color defaultColor;

    // Use this for initialization
	void Start () {
        rend = GetComponent<Renderer>();
        defaultColor = rend.material.color;
        generateNeighbours();
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
        else // added temporarly to create imPassable areas for pathfinding testing
        {
            imPassable = !imPassable;
            if (imPassable)
            {
                Rend.material.color = Color.black;
            }
            else
            {
                Rend.material.color = Color.white;
            }
        }
    }

    void GenerateNeighbours()
    {
        neighbours = new ListTile();

        // y+ (up)
        if (GridPosition.y > 0)
        {
            Vector2 n = new Vector2(GridPosition.x, GridPosition.y - 1);
            neighbours.Add(GameManager.Instance.map[(int)n.x][(int)n.y]);
        }

        // y- (down)
        if (GridPosition.y < GameManager.Instance.map.Count - 1)
        {
            Vector2 n = new Vector2(GridPosition.x, GridPosition.y + 1);
            neighbours.Add(GameManager.Instance.map[(int)n.x][(int)n.y]);
        }

        // x+ (right)
        if (GridPosition.x > 0)
        {
            Vector2 n = new Vector2(GridPosition.x - 1, GridPosition.y);
            neighbours.Add(GameManager.Instance.map[(int)n.x][(int)n.y]);
        }

        // x- (left)
        if (GridPosition.x < GameManager.Instance.map.Count - 1)
        {
            Vector2 n = new Vector2(GridPosition.x + 1, GridPosition.y);
            neighbours.Add(GameManager.Instance.map[(int)n.x][(int)n.y]);
        }
    }
}
