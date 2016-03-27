using UnityEngine;
using System.Collections;

public class Player : MonoBehaviour {

    public Vector3 moveDestination;
    public Vector2 GridPosition = Vector3.zero;
    public bool moving = false;
    public bool attacking = false;
    
    // these are static for now and will be converted when the classes for the RPG elements are added
    public int HP = 25;
    public int hitChance = 2; // base attack bonus!
    public int defenseChance = 15; // AC
    public int damageBase = 5;
    public int HitDie = 6;
    public int DamageReduction = 2; // DR valule (armour and shields and stuff)
    public int ActionPoints;

    public string Name;

    void Awake()
    {
        ActionPoints = 2;
        moveDestination = transform.position;
    }

	// Use this for initialization
	void Start () {
	}
	
	// Update is called once per frame
	void Update () {
	
	}
    public virtual void TurnUpdate()
    {
        if (ActionPoints <= 0)
        {
            ActionPoints = 2;
            moving = false;
            attacking = false;
            GameManager.Instance.NextTurn();
        }
    }
    public virtual void TurnOnGUI()
    {

    }
}
