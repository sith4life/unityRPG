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
	public override void Update () {
        base.Update();
    }

    public override void TurnUpdate()
    {
        // positionQueue stuff
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
        else
        {
            //priority queue
            List<Tile> attacktilesInRange = TileHighlight.FindHighlight(GameManager.instance.map[(int)gridPosition.x][(int)gridPosition.y], attackRange);
            List<Tile> movementToAttackTilesInRange = TileHighlight.FindHighlight(GameManager.instance.map[(int)gridPosition.x][(int)gridPosition.y], movementPerActionPoint + attackRange);
            List<Tile> movementTilesInRange = TileHighlight.FindHighlight(GameManager.instance.map[(int)gridPosition.x][(int)gridPosition.y], movementPerActionPoint + 1000);
            //attack if in range and with lowest HP
            if (attacktilesInRange.Where(x => GameManager.instance.players.Where(y => y.GetType() != typeof(AIPlayer) && y.HP > 0 && y != this && y.gridPosition == x.gridPosition).Count() > 0).Count() > 0)
            {
                var opponentsInRange = attacktilesInRange.Select(x => GameManager.instance.players.Where(y => y.GetType() != typeof(AIPlayer) && y.HP > 0 && y != this && y.gridPosition == x.gridPosition).Count() > 0 ? GameManager.instance.players.Where(y => y.gridPosition == x.gridPosition).First() : null).ToList();
                Player opponent = opponentsInRange.OrderBy(x => x != null ? -x.HP : 1000).First();

                GameManager.instance.removeTileHighlights();
                moving = false;
                attacking = true;
                GameManager.instance.highlightTilesAt(gridPosition, Color.red, attackRange);

                GameManager.instance.attackWithCurrentPlayer(GameManager.instance.map[(int)opponent.gridPosition.x][(int)opponent.gridPosition.y]);
            }
            //move toward nearest attack range of opponent
            else if (!moving && movementToAttackTilesInRange.Where(x => GameManager.instance.players.Where(y => y.GetType() != typeof(AIPlayer) && y.HP > 0 && y != this && y.gridPosition == x.gridPosition).Count() > 0).Count() > 0)
            {
                var opponentsInRange = movementToAttackTilesInRange.Select(x => GameManager.instance.players.Where(y => y.GetType() != typeof(AIPlayer) && y.HP > 0 && y != this && y.gridPosition == x.gridPosition).Count() > 0 ? GameManager.instance.players.Where(y => y.gridPosition == x.gridPosition).First() : null).ToList();
                Player opponent = opponentsInRange.OrderBy(x => x != null ? -x.HP : 1000).ThenBy(x => x != null ? TilePathFinder.FindPath(GameManager.instance.map[(int)gridPosition.x][(int)gridPosition.y], GameManager.instance.map[(int)x.gridPosition.x][(int)x.gridPosition.y]).Count() : 1000).First();

                GameManager.instance.removeTileHighlights();
                moving = true;
                attacking = false;
                GameManager.instance.highlightTilesAt(gridPosition, Color.blue, movementPerActionPoint, false);

                List<Tile> path = TilePathFinder.FindPath(GameManager.instance.map[(int)gridPosition.x][(int)gridPosition.y], GameManager.instance.map[(int)opponent.gridPosition.x][(int)opponent.gridPosition.y], GameManager.instance.players.Where(x => x.gridPosition != gridPosition && x.gridPosition != opponent.gridPosition).Select(x => x.gridPosition).ToArray());
                GameManager.instance.moveCurrentPlayer(path[(int)Mathf.Max(0, path.Count - 1 - attackRange)]);
            }
            //move toward nearest opponent
            else if (!moving && movementTilesInRange.Where(x => GameManager.instance.players.Where(y => y.GetType() != typeof(AIPlayer) && y.HP > 0 && y != this && y.gridPosition == x.gridPosition).Count() > 0).Count() > 0)
            {
                var opponentsInRange = movementTilesInRange.Select(x => GameManager.instance.players.Where(y => y.GetType() != typeof(AIPlayer) && y.HP > 0 && y != this && y.gridPosition == x.gridPosition).Count() > 0 ? GameManager.instance.players.Where(y => y.gridPosition == x.gridPosition).First() : null).ToList();
                Player opponent = opponentsInRange.OrderBy(x => x != null ? -x.HP : 1000).ThenBy(x => x != null ? TilePathFinder.FindPath(GameManager.instance.map[(int)gridPosition.x][(int)gridPosition.y], GameManager.instance.map[(int)x.gridPosition.x][(int)x.gridPosition.y]).Count() : 1000).First();

                GameManager.instance.removeTileHighlights();
                moving = true;
                attacking = false;
                GameManager.instance.highlightTilesAt(gridPosition, Color.blue, movementPerActionPoint, false);

                List<Tile> path = TilePathFinder.FindPath(GameManager.instance.map[(int)gridPosition.x][(int)gridPosition.y], GameManager.instance.map[(int)opponent.gridPosition.x][(int)opponent.gridPosition.y], GameManager.instance.players.Where(x => x.gridPosition != gridPosition && x.gridPosition != opponent.gridPosition).Select(x => x.gridPosition).ToArray());
                GameManager.instance.moveCurrentPlayer(path[(int)Mathf.Min(Mathf.Max(path.Count - 1 - 1, 0), movementPerActionPoint - 1)]);
            }
            // end turn
            else
            {
                ActionPoints = 2;
                moving = false;
                attacking = false;
                GameManager.Instance.NextTurn();
            }
        }
    }
    public override void TurnOnGUI()
    {
        base.TurnOnGUI();
    }
}
