#ifndef __EDGE_H__
#define __EDGE_H__

class Edge
{
public:
    int to;
    int value;

    Edge(int _to, int _value)
    {
        this->to = _to;
        this->value = _value;
    }
};


#endif
