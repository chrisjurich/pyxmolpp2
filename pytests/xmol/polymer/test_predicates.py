import pytest
import os

def make_polyglycine( chain_lengths, no_reserve=True):
    from pyxmolpp2.polymer import Frame
    from pyxmolpp2.polymer import ChainName
    from pyxmolpp2.polymer import AtomName
    from pyxmolpp2.polymer import ResidueName, ResidueId
    from pyxmolpp2.geometry import XYZ

    aid=1
    rid=1
    frame = Frame(0)
    for chainId, N in chain_lengths:
        if no_reserve:
            c = frame.emplace(ChainName(chainId))
        else:
            c = frame.emplace(ChainName(chainId),N)
        for i in range(N):
            if no_reserve:
                r = c.emplace(ResidueName("GLY"),ResidueId(rid))
            else:
                r = c.emplace(ResidueName("GLY"),ResidueId(rid),7)

            rid+=1
            for aname in ["N","H","CA","HA2","HA3","C","O"]:
                r.emplace(AtomName(aname),aid,XYZ(1,2,3))
                aid+=1

    return frame


def test_atom_name():
    from pyxmolpp2.polymer import aName
    frame = make_polyglycine([("A", 10)])

    assert frame.asAtoms.filter(aName == "CA").size == 10
    assert frame.asAtoms.filter(aName.is_in({"CA", "N"})).size == 20
    assert frame.asAtoms.filter(~aName.is_in({"CA", "N"})).size == 50
    assert frame.asAtoms.filter((aName == "CA") | (aName == "N")).size == 20


def test_residue_name():
    from pyxmolpp2.polymer import rName
    frame = make_polyglycine([("A", 10)])

    assert frame.asAtoms.filter(rName == "GLY").size == 70
    assert frame.asAtoms.filter(rName.is_in({"GLY", "LYS"})).size == 70
    assert frame.asAtoms.filter(~rName.is_in({"GLY"})).size == 0
    assert frame.asAtoms.filter((rName == "GLY") | (rName != "GLY")).size == 70

    assert frame.asResidues.filter(rName == "GLY").size == 10
    assert frame.asResidues.filter(rName.is_in({"GLY", "LYS"})).size == 10
    assert frame.asResidues.filter(~rName.is_in({"GLY"})).size == 0
    assert frame.asResidues.filter((rName == "GLY") | (rName != "GLY")).size == 10



def test_chain_name():
    from pyxmolpp2.polymer import cName
    frame = make_polyglycine([("A", 10),("B",20)])

    assert frame.asAtoms.filter(cName == "A").size == 10*7
    assert frame.asAtoms.filter(cName.is_in({"A", "B"})).size == 30*7
    assert frame.asAtoms.filter(~cName.is_in({"B"})).size == 10*7
    assert frame.asAtoms.filter((cName == "A") | (cName != "B")).size == 10*7

    assert frame.asResidues.filter(cName == "A").size == 10
    assert frame.asResidues.filter(cName.is_in({"A", "B"})).size == 30
    assert frame.asResidues.filter(~cName.is_in({"B"})).size == 10
    assert frame.asResidues.filter((cName == "A") | (cName != "B")).size == 10

    assert frame.asChains.filter(cName == "A").size == 1
    assert frame.asChains.filter(cName.is_in({"A", "B"})).size == 2
    assert frame.asChains.filter(~cName.is_in({"B"})).size == 1
    assert frame.asChains.filter((cName == "A") | (cName != "B")).size == 1


def test_atom_id():
    from pyxmolpp2.polymer import aId
    frame = make_polyglycine([("A", 10)])

    assert frame.asAtoms.filter(aId == 5).size == 1
    assert frame.asAtoms.filter(aId.is_in({1,2,3})).size == 3
    assert frame.asAtoms.filter(~aId.is_in({1,2,3})).size == 70-3
    assert frame.asAtoms.filter((aId == 2) | (aId == 3)).size == 2


def test_residue_id():
    from pyxmolpp2.polymer import rId, ResidueId, ResidueInsertionCode
    frame = make_polyglycine([("A", 10)])

    assert frame.asAtoms.filter(rId == 5).size == 1*7
    assert frame.asAtoms.filter(rId.is_in({1,2,3})).size == 3*7
    assert frame.asAtoms.filter(~rId.is_in({1,2,3})).size == 7*7
    assert frame.asAtoms.filter((rId == 2) | (rId == 3)).size == 2*7

    assert frame.asResidues.filter(rId == 5).size == 1
    assert frame.asResidues.filter(rId.is_in({1,2,3})).size == 3
    assert frame.asResidues.filter(~rId.is_in({1,2,3})).size == 7
    assert frame.asResidues.filter((rId == 2) | (rId == 3)).size == 2

    assert frame.asResidues.filter(rId == ResidueId(5,ResidueInsertionCode("A"))).size == 0


def test_chain_index():
    from pyxmolpp2.polymer import cIndex
    frame = make_polyglycine([("A", 10)])

    assert frame.asAtoms.filter(cIndex == 0).size == 70
    assert frame.asAtoms.filter(cIndex.is_in({0})).size == 70
    assert frame.asAtoms.filter(cIndex.is_in({1,2})).size == 0


    assert frame.asResidues.filter(cIndex == 0).size == 10
    assert frame.asResidues.filter(cIndex.is_in({0})).size == 10
    assert frame.asResidues.filter(cIndex.is_in({1,2})).size == 0


    assert frame.asChains.filter(cIndex == 0).size == 1
    assert frame.asChains.filter(cIndex == 1).size == 0